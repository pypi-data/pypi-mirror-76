# Overview
Python `shinobi` is an open-source data management and analytic toolkit. Right now, `shinobi` services users running a local or hosted instance of [Elasticsearch](elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html) by offering tools for easily ingesting, indexing, accessing, storing, visualizing, and analyzing data stored on an Elasticsearch cluster. In addition, `shinobi` services users with general, data agnostic statistical analytics to allow for facilitated machine learning at your fingertips. This project is still in development.

## Prerequisites
### Elasticsearch
Although `shinobi` users can leverage its data storage and analysis capabilities without a connection to an Elasticsearch cluster, it is recommended to access Elasticsearch to maximize the value of this package. The setup process for Elasticsearch is relatively straightforward and is well-documented with the following [setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html). Elasticsearch version 7.8.1 or higher is recommended.

## Quickstart
### Installation via `pip`
The `shinobi` library is active on PyPI, so it can be installed via `pip`:
```
pip install shinobi
```

### Manual Installation
Alternatively, users can clone [this repository](https://github.com/dykstal/shinobi) with Git and then build manually via:
```
git clone https://github.com/dykstal/shinobi.git
cd shinobi/tools
./build
source ../venvs/shinobi-env/bin/activate
```

## Examples
### Importing `shinobi`
Simply `import shinobi` in your python session.

### More to Come... :)
