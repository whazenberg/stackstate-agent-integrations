# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from .agent import (
    FAKE_API_KEY,
    get_agent_exe, get_agent_conf_dir,
    get_rate_flag, get_log_level_flag
)
from .config import (
    config_file_name, env_exists, locate_config_dir, locate_config_file, remove_env_data, write_env_data
)
from ..constants import get_root
from ...subprocess import run_command
from ...utils import path_join
from ..commands.console import echo_info


class DockerInterface(object):
    ENV_TYPE = 'docker'

    def __init__(
            self,
            check,
            env,
            base_package=None,
            config=None,
            metadata=None,
            agent_build=None,
            sts_url=None,
            api_key=None,
            cluster_name=None,
            env_vars=None
    ):
        self.check = check
        self.env = env
        self.env_vars = env_vars or {}
        self.base_package = base_package
        self.config = config or {}
        self.metadata = metadata or {}
        self.agent_build = agent_build
        self.api_key = api_key or FAKE_API_KEY
        self.sts_url = sts_url
        self.cluster_name = cluster_name

        self.container_name = 'stackstate_{}_{}'.format(self.check, self.env)
        self.config_dir = locate_config_dir(check, env)
        self.config_file = locate_config_file(check, env)
        self.config_file_name = config_file_name(self.check)

    def mount_dir(self, subdir):
        return '/home/{}'.format(subdir)

    @property
    def check_mount_dir(self):
        return self.mount_dir(self.check)

    @property
    def base_mount_dir(self):
        return '/home/stackstate_checks_base'

    @property
    def agent_command(self):
        return 'docker exec {} {}'.format(
            self.container_name,
            get_agent_exe()
        )

    def run_check(self, capture=False, rate=False, log_level=None):
        command = '{} check {}{}{}'.format(
            self.agent_command,
            self.check,
            ' {}'.format(get_rate_flag()) if rate else '',
            ' {} {}'.format(get_log_level_flag(), log_level) if log_level else '',
        )
        echo_info("\nCommand used for running the check: '{0}'\n".format(command))
        return run_command(command, capture=capture)

    def exists(self):
        return env_exists(self.check, self.env)

    def remove_config(self):
        remove_env_data(self.check, self.env)

    def write_config(self):
        write_env_data(self.check, self.env, self.config, self.metadata)

    def update_check(self):
        command_deps = [
            'docker', 'exec', self.container_name, 'pip', 'install', '-r',
            "{}/requirements.in".format(self.check_mount_dir)
        ]
        run_command(command_deps, capture=True, check=True)
        command = [
            'docker', 'exec', self.container_name, 'pip', 'install', '-e', self.check_mount_dir
        ]
        run_command(command, capture=True, check=True)

    def update_base_package(self):
        command = [
            'docker', 'exec', self.container_name, 'pip', 'install', '-e', self.base_mount_dir
        ]
        run_command(command, capture=True, check=True)
        # Install shared libraries
        with open(path_join(get_root(), "shared_libraries.in"), "r") as shared_file:
            for line in shared_file:
                shared_lib = line.strip()
                command = [
                    'docker', 'exec', self.container_name, 'pip', 'install', '-e', self.mount_dir(shared_lib)
                ]
                run_command(command, capture=True, check=True)

    def update_agent(self):
        if self.agent_build:
            run_command(['docker', 'pull', self.agent_build], capture=True, check=True)

    def start_agent(self):
        if not self.agent_build:
            return

        env_vars = {
            # Agent 6 will simply fail without an API key
            'STS_API_KEY': self.api_key,
            # We still need this trifold, this should be improved
            'STS_STS_URL': self.sts_url,
            # Set the Kubernetes Cluster Name for k8s integrations
            'CLUSTER_NAME:': self.cluster_name,
            # Avoid clashing with an already running agent's CMD port
            'STS_CMD_PORT': 4999,
            # Disable trace agent
            'STS_APM_ENABLED': 'false',
            # Enable debugging level
            'STS_LOG_LEVEL': 'DEBUG',
            # Don't write .pyc, needed to fix this issue (only Python 2):
            # When reinstalling a package, .pyc are not cleaned correctly. The issue is fixed by not writing them
            # in the first place.
            # More info: https://github.com/DataDog/integrations-core/pull/5454
            # TODO: Remove PYTHONDONTWRITEBYTECODE env var when Python 2 support is removed
            'PYTHONDONTWRITEBYTECODE': "1",
        }
        env_vars.update(self.env_vars)

        volumes = [
            # Mount the config directory, not the file, to ensure updates are propagated
            # https://github.com/moby/moby/issues/15793#issuecomment-135411504
            '{}:{}'.format(self.config_dir, get_agent_conf_dir(self.check)),
            # Mount the check directory
            '{}:{}'.format(path_join(get_root(), self.check), self.check_mount_dir),
        ]
        volumes.extend(self.metadata.get('docker_volumes', []))

        command = [
            'docker',
            'run',
            # Keep it up
            '-d',
            # Ensure consistent naming
            '--name', self.container_name,
            # Ensure access to host network
            '--network', 'host',
        ]
        for volume in volumes:
            command.extend(['-v', volume])

        # Any environment variables passed to the start command
        for key, value in sorted(env_vars.items()):
            command.extend(['-e', '{}={}'.format(key, value)])

        if self.base_package:
            # Mount the check directory
            command.append('-v')
            command.append('{}:{}'.format(self.base_package, self.base_mount_dir))

            # Include shared libraries
            with open(path_join(get_root(), "shared_libraries.in"), "r") as shared_file:
                for line in shared_file:
                    shared_lib = line.strip()
                    command.append('-v')
                    command.append('{}:{}'.format(path_join(get_root(), shared_lib), self.mount_dir(shared_lib)))

        # The chosen tag
        command.append(self.agent_build)

        echo_info("\nCommand used to start the agent env: '{0}'\n".format(" ".join(command)))
        return run_command(command, capture=True)

    def stop_agent(self):
        # Only error for exit code if config actually exists
        run_command(['docker', 'stop', self.container_name], capture=True, check=self.exists())
        run_command(['docker', 'rm', self.container_name], capture=True, check=self.exists())

    def restart_agent(self):
        return run_command(['docker', 'restart', self.container_name], capture=True)


def get_docker_networks():
    command = ['docker', 'network', 'ls', '--format', '{{.Name}}']
    lines = run_command(command, capture='out', check=True).stdout.splitlines()

    return [line.strip() for line in lines]
