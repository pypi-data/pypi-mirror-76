"""
graph-theory
"""
build_tag = "d86fdf1773f412430c8f94adc43a81c22268154739734b15dfdd435cab87a26b"
from setuptools import setup
from pathlib import Path


folder = Path(__file__).parent
file = "README.md"
readme = folder / file
assert isinstance(readme, Path)
assert readme.exists(), readme
with open(str(readme), encoding='utf-8') as f:
    long_description = f.read()

keywords = list({
    'complex-networks', 'discrete mathematics', 'graph', 'Graph Theory', 'graph-algorithms', 'graph-analysis',
    'graph-generation', 'graph-theory', 'graph-visualization', 'graphs', 'math', 'Mathematics', 'maths',
    'minimum-spanning-trees', 'network', 'Networks', 'optimization', 'python', 'shortest-path', 'tsp', 'tsp-solver',
    'assignment problem', 'flow-problem', 'hash', 'graph-hash', 'random graph', 'search', 'cycle', 'path',
    'component', 'components', 'adjacency', 'matrix', 'all pairs shortest path', 'finite state machine', 'fsm'
})

keywords.sort(key=lambda x: x.lower())


setup(
    name="graph-theory",
    version="2020.8.14.60559",
    url="https://github.com/root-11/graph-theory",
    license="MIT",
    author="Bjorn Madsen",
    author_email="bjorn.madsen@operationsresearchgroup.com",
    description="A graph library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=keywords,
    packages=["graph"],
    include_package_data=True,
    data_files=[(".", ["LICENSE", "README.md"])],
    platforms="any",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)


