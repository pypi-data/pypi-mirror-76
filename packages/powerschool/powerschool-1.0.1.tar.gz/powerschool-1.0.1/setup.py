# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powerschool']

package_data = \
{'': ['*']}

install_requires = \
['fiql_parser>=0.15,<0.16',
 'oauthlib>=3.1.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'requests_oauth>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'powerschool',
    'version': '1.0.1',
    'description': 'powerschool is a Python client for the PowerSchool API',
    'long_description': "# PowerSchool\npowerschool is a Python client for the [PowerSchool SIS](https://www.powerschool.com/solutions/student-information-system/powerschool-sis) API\n\n## Installation\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install powerschool.\n```bash\npip install powerschool\n```\n\n## Getting Started\n1. Ensure you have a valid [plugin](https://support.powerschool.com/developer/#/page/plugin-xml) installed with the proper data access provisioned for your purposes.\n   \n2. Instantiate the client by passing the host name of your server.\n    ```python\n    import powerschool\n    ps = powerschool.PowerSchool('my.host.name')\n    ```\n\n3. Authorize the client using:\n    - client credentials (tuple)\n    ```python\n    my_credentials = (client_id, client_secret)\n    ps.authorize(client_credentials=my_credentials)\n    ```\n\n    - a previously saved access token (dict)\n    ```python\n    with open(token_file, 'r') as f:\n        my_token = json.load(f)\n    \n    ps.authorize(access_token=my_token)\n    ```\n\n## Usage\n>*Refer to the [docs](https://support.powerschool.com/developer/#/page/data-access) for full functionality, including resources, searching, and pagination.*\n\n**Instantiate a table or PowerQuery object:**\n```python\nschools_table = ps.get_schema_table('schools')\n\npowerquery = ps.get_named_query('com.pearson.core.student.search.get_student_basic_info')\n```\n\n**Get the record count for a table:**\n```python\nschools_table.count()\n```\n\n**Query all records, all columns on a table:**\n>*Pagination is handled automatically by the client. However, you can manually pass `pagesize` and `page` parameters, should you choose.*\n```python\nschools_table.query()\n```\n\n**Query all records on a table, with filter and columns list:**\n```python\nparams = {\n    'q': 'id=ge=10000',\n    'projection': 'school_number,abbreviation',\n}\nschools_table.query(**params)\n```\n\n**Query a specific record on a table:**\n```python\nschools_table.query(dcid=123)\n```\n\n**Execute a PowerQuery, passing arguments in the body:**\n```python\npayload = {\n    'studentdcid': '5432',\n}\npowerquery.query(body=payload)\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## Notice\nPowerSchool® is a registered trademark in the U.S. and/or other countries owned by PowerSchool Education, Inc. or its affiliates. PowerSchool® is used under license.\n",
    'author': 'Charlie Bini',
    'author_email': 'cbini87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TEAMSchools/powerschool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
