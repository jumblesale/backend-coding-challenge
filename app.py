import os

from unbabel.config import dev_config, test_config

config = {
    'test': test_config,
    'dev':  dev_config,
}[os.environ.get('ENVIRONMENT', 'test')]

app = config()

if __name__ == '__main__':
    app.run()
