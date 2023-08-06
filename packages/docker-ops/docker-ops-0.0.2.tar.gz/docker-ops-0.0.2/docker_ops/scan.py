#!/usr/bin/env python

import docker
import json
import hashlib
import os
import tempfile
import typing

REGISTRY_DOMAIN = os.environ['IMAGE_REGISTRY_DOMAIN']
PROJECT_DIR = os.getcwd()
ENCODING = 'utf-8'
PWN = typing.TypeVar('PWN')

class Version:
    def __init__(self: PWN, version: str) -> None:
        version = version or '0.0.0'
        self._major = int(version.split('.', 1)[0])
        self._minor = int(version.split('.', 2)[1])
        self._minor_minor = int(version.rsplit('.', 1)[1])

    def inc_minor_minor(self: PWN) -> None:
        self._minor_minor = self._minor_minor + 1

    def get_version(self: PWN) -> None:
        return f'{self._major}.{self._minor}.{self._minor_minor}'

    def __repr__(self:PWN) -> str:
        return f'Version[{self.get_version()}]'

class Hash:
    def __init__(self: PWN, dockerfile_path: str) -> str:
        if not os.path.exists(dockerfile_path):
            raise IOError(f'Unable to load Dockerfile[{dockerfile_path}]')

        with open(dockerfile_path, 'rb') as stream:
            self._file_data = stream.read().decode(ENCODING)

    def get_hash(self: PWN) -> str:
        return hashlib.sha256(self._file_data.encode(ENCODING)).hexdigest()

    def __repr__(self: PWN) -> str:
        return f'Build Hash: {self.get_hash()}'

class Docker:
    def __init__(self: PWN, docker_filepath: str) -> None:
        self._client = docker.APIClient(base_url='unix://var/run/docker.sock')
        # self._client = docker.from_env()
        # self._client = docker.APIClient(base_url='tcp://127.0.0.1:2375')
        self._docker_filepath = docker_filepath

    def _stream_output(self: PWN, generator: typing.Any) -> None:
        while True:
            try:
                output = generator.__next__()
                output = json.loads(output.decode(ENCODING))
                if 'stream' in output.keys():
                    print(output['stream'].strip('\n'))
            except StopIteration:
                break

    def build(self: PWN, build_path: str, registry_domain: str, build_name: str, version: str) -> None:
        build_tag = f'{registry_domain}/{build_name}:{version}'
        build_path = os.path.join(build_path, build_name)
        generator = self._client.build(path=build_path, dockerfile=self._docker_filepath, tag=build_tag)
        self._stream_output(generator)

    def _stream_push_output(self: PWN, line: typing.Any) -> None:
        if 'id' in line.keys() and 'progress' in line.keys():
            print(line['id'], line['status'], line['progress'])

        elif 'id' in line.keys():
            print(line['id'], line['status'])

        elif 'aux' in line.keys():
            print(line['aux']['Tag'], line['aux']['Digest'], line['aux']['Size'])

        elif 'status' in line.keys():
            print('Status: ', line['status'])

        else:
            print('Other: ', line)

    def push(self: PWN, registry_domain: str, build_name: str, version: str) -> None:
        build_name = f'{registry_domain}/{build_name}'
        for line in self._client.push(build_name, version, stream=True, decode=True):
            self._stream_push_output(line)

    def sync_latest(self: PWN, registry_domain: str, build_name: str, version: str) -> None:
        build_name = f'{registry_domain}/{build_name}'
        build_source = f'{build_name}:{version}'
        self._client.tag(build_source, build_name, 'latest')
        for line in self._client.push(build_name, 'latest', stream=True, decode=True):
            self._stream_push_output(line)

class BuildInfo:
    KEYS = ['version', 'name', 'hash']
    def __init__(self: PWN, build_info_dir: str) -> None:
        build_info_filename = 'build-info.json'
        self.build_info_path = os.path.join(build_info_dir, build_info_filename)
        if not os.path.exists(self.build_info_path):
            self._build_info = {
                'name': os.path.dirname(self.build_info_path).rsplit('/', 1)[1]
            }

        else:
            with open(self.build_info_path, 'rb') as stream:
                self._build_info = json.loads(stream.read().decode(ENCODING))

    @property
    def name(self: PWN) -> str:
        return self._build_info['name']

    @property
    def version(self: PWN) -> Version:
        if hasattr(self, '_version'):
            return self._version

        self._version = Version(self._build_info.get('version', None))
        return self._version

    @property
    def hash(self: PWN) -> Hash:
        if hasattr(self, '_hash'):
            return self._hash

        docker_filepath = os.path.dirname(self.build_info_path)
        docker_filepath = os.path.join(docker_filepath, 'Dockerfile')
        self._hash = Hash(docker_filepath)
        return self._hash

    @property
    def docker(self: PWN) -> Docker:
        docker_filepath = os.path.dirname(self.build_info_path)
        docker_filepath = os.path.join(docker_filepath, 'Dockerfile')
        if hasattr(self, '_docker'):
            return self._docker

        self._docker = Docker(docker_filepath)
        return self._docker

        
    def __repr__(self: PWN) -> str:
        return f'{self.name} {self.version.get_version()}'

    def new_build_required(self: PWN) -> bool:
        return self._build_info.get('hash', None) != self.hash.get_hash()

    def store(self: PWN) -> None:
        self._build_info['hash'] = self.hash.get_hash()
        self._build_info['version'] = self.version.get_version()
        data = json.dumps(self._build_info, indent=2).encode(ENCODING)
        with open(self.build_info_path, 'wb') as stream:
            stream.write(data)

def find_new_builds(image_dir: str) -> typing.List[BuildInfo]:
    new_builds = []
    for root, dirnames, filenames in os.walk(image_dir):
        for dirname in dirnames:
            dockerfile_path = os.path.join(root, dirname, 'Dockerfile')
            if not os.path.exists(dockerfile_path):
                continue
    
            build_data_path = os.path.join(root, dirname, 'build.json')
            if not os.path.exists(build_data_path):
                new_builds.append(BuildInfo(os.path.join(root, dirname)))
                continue
    
            import pdb; pdb.set_trace()
            import sys; sys.exit(1)

    return new_builds

def scan_and_build(directory_path: str) -> None:
    for build_info in find_new_builds(directory_path):
        if build_info.new_build_required():
            build_info.version.inc_minor_minor()
            build_info.docker.build(directory_path, REGISTRY_DOMAIN, build_info.name, build_info.version.get_version())
            build_info.docker.push(REGISTRY_DOMAIN, build_info.name, build_info.version.get_version())
            build_info.docker.sync_latest(REGISTRY_DOMAIN, build_info.name, build_info.version.get_version())
    
        build_info.store()

