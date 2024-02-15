import scrapy
import json

class SRealitypider(scrapy.Spider):
    name = 'serality'
    start_urls = [
        'https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500'
    ]
    custom_settings = {
            'ITEM_PIPELINES': {'scrapy_app.pipelines.PostgresPipeline': 300},
            'LOG_LEVEL': 'INFO'
        }
    
    def parse(self, response):
        # Load the JSON response
        data = json.loads(response.text)
        # Extract data for each estate
        for estate in data.get('_embedded', {}).get('estates', []):
            title = estate.get('name')
            images = estate.get('_links', {}).get('images', [])
            first_image_url = images[0].get('href') if images else None

            yield {
                'title': title,
                'first_image_url': first_image_url
            }
