# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['easel', 'easel.main', 'easel.site']

package_data = \
{'': ['*'],
 'easel.main': ['assets/static/css/*',
                'assets/static/fonts/Fira_Code_v5.2.zip',
                'assets/static/fonts/Fira_Code_v5.2.zip',
                'assets/static/fonts/Fira_Code_v5.2.zip',
                'assets/static/fonts/Fira_Code_v5.2/README.txt',
                'assets/static/fonts/Fira_Code_v5.2/README.txt',
                'assets/static/fonts/Fira_Code_v5.2/README.txt',
                'assets/static/fonts/Fira_Code_v5.2/fira_code.css',
                'assets/static/fonts/Fira_Code_v5.2/fira_code.css',
                'assets/static/fonts/Fira_Code_v5.2/fira_code.css',
                'assets/static/fonts/Fira_Code_v5.2/specimen.html',
                'assets/static/fonts/Fira_Code_v5.2/specimen.html',
                'assets/static/fonts/Fira_Code_v5.2/specimen.html',
                'assets/static/fonts/Fira_Code_v5.2/ttf/*',
                'assets/static/fonts/Fira_Code_v5.2/variable_ttf/*',
                'assets/static/fonts/Fira_Code_v5.2/woff/*',
                'assets/static/fonts/Fira_Code_v5.2/woff2/*',
                'assets/static/fonts/PT_Sans.zip',
                'assets/static/fonts/PT_Sans.zip',
                'assets/static/fonts/PT_Sans.zip',
                'assets/static/fonts/PT_Sans/*',
                'assets/static/fonts/Roboto_Condensed.zip',
                'assets/static/fonts/Roboto_Condensed.zip',
                'assets/static/fonts/Roboto_Condensed.zip',
                'assets/static/fonts/Roboto_Condensed/*',
                'assets/static/images/bullet.png',
                'assets/static/images/bullet.png',
                'assets/static/images/bullet.png',
                'assets/static/images/menu-mobile-close.png',
                'assets/static/images/menu-mobile-close.png',
                'assets/static/images/menu-mobile-close.png',
                'assets/static/images/menu-mobile-open.png',
                'assets/static/images/menu-mobile-open.png',
                'assets/static/images/menu-mobile-open.png',
                'assets/static/js/*',
                'assets/templates/base.jinja2',
                'assets/templates/base.jinja2',
                'assets/templates/base.jinja2',
                'assets/templates/base.jinja2',
                'assets/templates/base.jinja2',
                'assets/templates/macros.jinja2',
                'assets/templates/macros.jinja2',
                'assets/templates/macros.jinja2',
                'assets/templates/macros.jinja2',
                'assets/templates/macros.jinja2',
                'assets/templates/menu.jinja2',
                'assets/templates/menu.jinja2',
                'assets/templates/menu.jinja2',
                'assets/templates/menu.jinja2',
                'assets/templates/menu.jinja2',
                'assets/templates/page.jinja2',
                'assets/templates/page.jinja2',
                'assets/templates/page.jinja2',
                'assets/templates/page.jinja2',
                'assets/templates/page.jinja2',
                'assets/templates/style.jinja2',
                'assets/templates/style.jinja2',
                'assets/templates/style.jinja2',
                'assets/templates/style.jinja2',
                'assets/templates/style.jinja2']}

install_requires = \
['flask>=1.1.2,<2.0.0',
 'markdown>=3.2.2,<4.0.0',
 'pymdown-extensions>=7.1,<8.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['_easel = src.easel.cli:cli', 'easel = easel.cli:cli']}

setup_kwargs = {
    'name': 'easel',
    'version': '1.0.0',
    'description': 'Showcasing work for the lazy. Built on Flask, YAML, Markdown and directories.',
    'long_description': '# Easel\n\nShowcasing work for the lazy. Built on Flask, YAML, Markdown and directories.\n\n## Installation\n\n### Create an environment\n\nCreate a project directory and a venv directory within:\n\n``` shell\n$ mkdir my-easel\n$ cd my-easel\n$ python3 -m venv venv\n```\n\n### Activate the environment\n\nBefore you work on your project, activate the corresponding environment:\n\n``` shell\n$ source venv/bin/activate\n```\n\nYour shell prompt will change to show the name of the activated environment.\n\n### Install Easel\nWithin the activated environment, use the following command to install Easel:\n\n``` shell\n$ pip install easel\n```\n\nEasel is now installed.\n\n\n## A Lazy Site\n\n### Create a site\n\nCreate a site directory and a `site.yaml` file:\n\n``` shell\n$ mkdir my-site\n$ cd my-site\n$ touch site.yaml\n```\n\nAdd the following to the `site.yaml` file:\n\n``` yaml\n# my-easel/my-site/site.yaml\n\ntitle: my-easel\nfavicon:\nyear: 2020\nname: My Name\n\npage:\n  width:\n\ncolors:\n  accent-base:\n  accent-light:\n\nmenu:\n  width:\n  align:\n  header:\n    label: my-easel\n    image:\n      path:\n      width:\n      height:\n  items:\n    - type: link-page\n      label: my-page\n      links-to: my-page\n```\n\nEvery site requires a `site.yaml` in the site\'s root directory. It\'s used to configure general site attributes namely the menu. Note that none of the items require a value, however all the items **must** be present. For example, `menu:items` can be an empty list, Easel will render no menu in this case. However if `menu:items` is missing a `ConfigError` will be thrown.\n\nNote that under `menu:items` we have a single item with the attribute `links-to` set to `my-page`. This is a path relative to the `pages` directory referring to the directory `my-page` we will be making shortly. Note that `links-to` always requires a path relative to the `pages` directory.\n\nOur Easel directory should now look like this:\n\n``` shell\nmy-easel\n├── my-site\n│   └── site.yaml\n└── venv\n```\n\n### Create a page\n\nCreate a page directory and a `page.yaml` file:\n\n``` shell\n$ mkdir my-page\n$ cd my-page\n$ touch page.yaml\n```\n\n\nAdd the following to the `page.yaml` file:\n\n``` yaml\n# my-easel/my-site/my-page/page.yaml\n# Lazy Page\n\n# Specify this page is the \'landing\' page.\nis-landing: true\n\n# Page type.\ntype: lazy\n\n# Lazy Page options.\noptions:\n  show-captions: true\n```\n\nEach page directory **must** contain a `page.yaml` file. In the same way that `site.yaml` configures the site, `page.yaml` configures the page. For this page we will do the laziest thing possible, create a `Lazy` page. This particular type of page auto populates its contents from the contents of its respective folder sorted alphabetically by the absolute path of each item.\n\nOur Easel directory should now look like this:\n\n``` shell\nmy-easel\n├── my-site\n│   ├── site.yaml\n│   └── pages\n│       └── my-page\n│           └── page.yaml\n└── venv\n```\n\nNow make sure to add some content: images, videos etc to the `my-page` directory:\n\n``` shell\nmy-easel\n├── my-site\n│   ├── site.yaml\n│   └── pages\n│       └── my-page\n│           ├── page.yaml\n│           ├── image-01.jpg\n│           ├── image-02.jpg\n│           ├── video.mp4\n│           └── ...\n└── venv\n```\n\n## A Minimal Application\n\nA minimal Easel application looks something like this:\n\n``` python\nfrom easel import Easel\n\neasel = Easel("my-site")\n\nif __name__ == "__main__":\n    easel.run()\n```\nNote that `my-site` refers to the directory `my-site`. We\'re providing a relative path here, telling Easel that our site directory is in the same directory as our application.\n\nNow save it as `run.py` in your `my-easel` directory next to your `my-site` directory.\n\nFinally, our Easel directory should look like this:\n\n``` shell\nmy-easel\n├── run.py\n├── my-site\n│   ├── site.yaml\n│   └── pages\n│       ├── my-page\n│       │   ├── page.yaml\n│       │   ├── image-001.jpg\n│       │   ├── image-002.jpg\n│       │   └── ...\n│       └── ...\n└── venv\n```\n\nTo run the application simply run the script.\n\n``` shell\n$ python run.py\n * Running on http://127.0.0.1:5000/\n```\n\nSo what did that code do?\n\n+ First we imported the Easel class. An instance of this class will hold our Flask application.\n+ Next we create an instance of this class. The first argument is the path to the directory containing your site along with its config files, pages and contents.\n+ Finally we place `easel.run()` in a guard statement so we can run a local development server when we directly run our script.\n\nThis launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. For deployment options see [Flask Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).\n\n\nNow head over to http://127.0.0.1:5000/, and you should see your beautiful work greeting.\n\n\n<!-- TODO: Create easel-demo and link here. -->\n\n\n# API\n\n## Custom Types\n\n``` python\n# Import Easel\'s Page, Menu and Content factories.\nfrom easel.site.pages import page_factory\nfrom easel.site.menus import menu_factory\nfrom easel.site.contents import content_factory\n\n# Import your custom types.\nfrom .custom import CustomPage, CustomMenu, CustomContent\n\n# Register your custom types.\npage_factory.register_page_type("custom-page", CustomPage)\nmenu_factory.register_menu_type("custom-menu", CustomMenu)\ncontent_factory.register_content_type("custom-content", CustomContent)\n```\n\n## Custom Assets (templates & static files)\n\n``` python\neasel = Easel(\n    site="my-site",\n    custom_assets="my-custom-assets",\n)\n```\n\nThe assets directory **must** follow the following structure.\n\n``` shell\nmy-custom-assets\n│\n├── templates\n│   ├── page.jinja2\n│   └── ...\n│\n└── static\n    ├── css\n    ├── js\n    ├── fonts\n    └── images\n\n```\nAdditionally it must contain a `page.jinja2` template in the `templates` directory. This is the entry-point for rendering pages. See `easel.main.views.render_page` and `easel.main.views.page_landing`.\n\n\n# Links / Resources\n\n+ Releases: https://pypi.org/project/easel/\n+ Flask documentation: https://github.com/pallets/flask',
    'author': 'Shant Ergenian',
    'author_email': 'shant.ergenian@gmail.com',
    'maintainer': 'Shant Ergenian',
    'maintainer_email': 'shant.ergenian@gmail.com',
    'url': 'https://github.com/tnahs/easel',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
