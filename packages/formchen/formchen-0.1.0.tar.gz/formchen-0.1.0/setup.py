# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formchen']

package_data = \
{'': ['*'], 'formchen': ['tests/*']}

install_requires = \
['gridchen>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'formchen',
    'version': '0.1.0',
    'description': 'Generate HTML forms and bind hierarchical and tabular data.',
    'long_description': 'Generate HTML forms and bind hierarchical and tabular data with the help of [JSON Schema](https://json-schema.org).\n\nForm-Chen supports master-detail relationships and undo/redo transaction management.\n\nIt uses [grid-chen](https://github.com/decatur/grid-chen) to produce Excel-like web-components for\ntabular (aka table/grid/matrix) data. \n\nEdits on the original object are emitted as standard [JSON Patch](https://tools.ietf.org/html/rfc6902),\nwhich can be directly passed to the back end.\n\nOptionally, object properties can be specified by [JSON Pointers](https://tools.ietf.org/html/rfc6901) to be bound to given HTML-elements.\n\nForm-Chen is written in plain EcmaScript 2017 modules and can be directly imported as such with any modern browser.\n\n# Usage\n\n![usage](usage.png)\n\n```html\n<div class="form-chen">\n    <!-- JSON Path to root element -->\n    <div id="/person"></div>\n    <!-- JSON Path to root vip property -->\n    <span style="font-size: x-large" id="/person/vip"></span>\n</div>\n```\n\n```javascript\n    import {createFormChen} from "./webcomponentwebcomponent.js"\n\n    const schema = {\n        title: \'Person\',\n        pathPrefix: \'/person\',\n        type: \'object\',\n        properties: {\n            name: {\n                title: \'Full Name of Person\', type: \'string\'\n            },\n            dateOfBirth: {\n                title: \'Date of Birth\', type: \'string\', format: \'full-date\'\n            },\n            vip: {\n                type: \'boolean\'\n            }\n        }\n    };\n\n    const data = {\n        name: \'Frida Krum\',\n        dateOfBirth: \'2019-01-01T00:00Z\',\n        vip: true\n    };\n\n    createFormChen(schema, data);\n```\n\n# Demos\n\nSee https://decatur.github.io/form-chen\n\n# Read Only\n\nAt any level, the schema can be marked `readOnly:true|false`, the default value being `false`.\nThe `readOnly` property is inherited by sub-schemas. \n\n# DOM Api and CSS Styling\n\nThe form is generated as a flat list of paired elements. The input elements are generated with the document ID corresponding to the JSON Pointer to its value.\n\nPairs           | Semantic\n----------------|-----------\n&lt;label/&gt; &lt;input&gt;     | For all scalar fields\n&lt;label/&gt; &lt;select&gt;    | For all scalar fields having an enum type\n&lt;label/&gt; &lt;checkbox&gt;  | For all scalar boolean fields\n&lt;label&gt; &lt;grid-chen/&gt; &lt;/label&gt;| For all grid fields\n&lt;label class=error/&gt;                   | For errors\n\nIn case a field has a unit, then the label will have a nested &lt;span class=unit/&gt; element.\n\nNo direct element style is applied.\n\nBased on this flat list of paired elements, the layout can be tweaked using CSS Column Layout, CSS Grid Layout or CSS Flex Layout, or whatever. See the demos for examples.\n\n# JavaScript Api\n\nPlease see the source code of the demos or [form-chen TypeScript Definitions](formchen/formchen.d.ts) for the public JavaScript Api.\n\n# Development\n\nForm-Chen is written in plain EcmaScript 2017 modules with JSDocs type hinting.\nThere is no overhead related to transpiling or packing.\nAs tool I recommend either vscode or one of the JetBrains IDEs (WebStorm, PyCharm).\n',
    'author': 'Wolfgang Kühn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decatur/form-chen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
