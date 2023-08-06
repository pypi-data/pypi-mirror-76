# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkquick', 'vkquick.annotypes', 'vkquick.tools', 'vkquick.validators']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'attrdict>=2.0.1,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'pygments>=2.6.1,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0',
 'watchdog>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['bot = vkquick.console:bot']}

setup_kwargs = {
    'name': 'vkquick',
    'version': '0.2.7',
    'description': 'Package for quick writing vk chat bots',
    'long_description': '> __vkquick__ — Это асинхронный фреймворк для разработки _легкоподдерживаемых_ чат-ботов ВКонтакте на Python\n\n## Почему vkquick?\nОсновная задача vkquick — обеспечить разработчика бота максимально _автоматизированным_ функционалом настолько, насколько это возможно, при этом оставляя возможность полного управления. Терминальный инструмент, позволяющий создавать команду буквально в одну строку и автоматически перезагружающий бота при изменениях в коде для комфортной разработки наряду с красочным режимом дебага, асинхронный код, выглядящий как синхронный и минималистичный синтаксис распарсинга команд вместо 1000 if, а также вагон полезных инструментов для _частовстречающихся_ кейсов позволяют практически не задумываться над _излишней_ работой с API и прочей рутинной работой, а сконцентрировать внимание именно на построении логики обработки.\n\nДля обычного бота, отвечающего на ваше сообщение, Вам нужно написать ровно 0 строк кода на Python. Не верите? Убедитесь в этом сами [на сайте нашей документации](https://vkquick.github.io/installation/)!\n',
    'author': 'Kurbatov Yan',
    'author_email': 'deknowny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rhinik/vkquick',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
