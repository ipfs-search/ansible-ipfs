# ansible-ipfs
Ansible collection for IPFS.

## Testing
This collection uses [molecule]() for testing.

### Install testing dependencies
1. Install Docker
2. Install packages for dependencies:
   a) Ubuntu: `sudo apt-get install python3-pip libssl-dev`
   b) CentOS: `sudo dnf install -y gcc python3-pip python3-devel openssl-devel python3-libselinux`
4. Install [pipenv](https://pipenv.pypa.io/en/latest/): `pip install pipenv` (or manually install dependencies with `pip install molecule[ansible,lint,docker]`)
5. Install Python dependencies: `pipenv install`

### Running tests
1. Start Docker
2. Activate pipenv: `pipenv shell`
2. Run tests: `molecule test`

## License
ansible-ipfs is dual-licensed under Apache 2.0 and MIT terms:

- Apache License, Version 2.0, ([LICENSE-APACHE](https://github.com/ipfs-search/ansible-ipfs/blob/main/LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](https://github.com/ipfs-search/ansible-ipfs/blob/main/LICENSE-MIT) or http://opensource.org/licenses/MIT)
