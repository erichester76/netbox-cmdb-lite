# NetBox CMDB Lite

NetBox CMDB Lite is a lightweight Configuration Management Database (CMDB) plugin for NetBox.

## Features

- Manage object types and their attributes
- Create and manage generic objects
- Define and manage relationships between objects

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/clemson-netbox/netbox_cmdb_lite.git
    ```

2. Install the plugin:
    ```sh
    cd netbox_cmdb_lite
    pip install .
    ```

3. Enable the plugin in your `netbox/configuration.py`:
    ```python
    PLUGINS = ['netbox_cmdb_lite']
    ```

4. Run migrations:
    ```sh
    python3 manage.py migrate
    ```

## Usage

- Access the plugin via the NetBox UI under the "CMDB Lite" section.
- Create and manage object types, generic objects, and relationships.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
