import json

from itemadapter import ItemAdapter
import re


class AptekaPipeline:
    def process_item(self, item, spider):
        item['assets'] = self.process_assets(item['assets'], item['RPC'])
        item['price_data'] = self.process_price(item['price_data'])
        item['section'] = self.process_section(item['section'])
        item['title'] = self.process_title(item['title'])
        item['metadata'] = self.process_metadata(item['metadata'], item['RPC'], item['title'])

        line = json.dumps(dict(item)) + ",\n"
        with open('result.json', 'a+') as f:
            content = json.dumps(line)
            f.write(content)

        return item

    def removing_spaces(self, value):
        return value.strip()

    def removing_spaces_in_list(self, data_list):
        return [self.removing_spaces(value) for value in data_list]

    def process_price(self, price):
        price = self.removing_spaces_in_list(price)

        price_dict = {}
        price_for_process = []
        for value in price:
            value = value.replace(' ', '')
            value_re = re.findall(r'[0-9]*\.[0-9]*', value)
            price_for_process.append(*value_re)

        value_min = float(min(price_for_process))
        value_max = float(max(price_for_process))
        discount = 0
        if value_max != value_min:
            discount = 100 - value_min / (value_max / 100)
            discount = f'Скидка {discount:.0f}%'

        price_dict['current'] = value_min
        price_dict['original'] = value_max
        price_dict['sale_tag'] = discount

        return price_dict

    def process_assets(self, assets, RPC):
        url = "https://apteka-ot-sklada.ru"
        url_main_image = f"{url}/images/goods/{RPC}.jpg"
        assets_dict = {}
        images = []

        # Очищаем от повторений фото
        for i in assets:
            if i not in images:
                images.append(i)

        # Делаем актуальные ссылки
        for value in range(len(images)):
            images[value] = f"{url}{images[value]}"

        assets_dict["main_image"] = url_main_image
        assets_dict["set_images"] = images
        assets_dict["view360"] = []
        assets_dict["video"] = []
        return assets_dict

    def process_section(self, section):
        section = section[2:]
        return section

    def process_title(self, title):

        title_replace = title.replace(' ', '')
        title_re = re.findall(r"[0-9]+..", title_replace)

        if title_re:
            title = f"{title}, {title_re[0]}"
        return title

    def process_metadata(self, metadata, product_code, title):
        metadata_dict = {}
        metadata_str = ''
        country_of_origin = metadata[0]
        del metadata[0]

        for value in metadata:
            metadata_str += f"\n{value.strip()}"

        volume = title.split(',')
        volume = volume[-1]

        metadata_dict['__description'] = metadata_str
        metadata_dict['COUNTRY_OF_ORIGIN'] = country_of_origin
        metadata_dict['PRODUCT_CODE'] = product_code
        metadata_dict['VOLUME'] = volume

        return metadata_dict
