# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AptekaPipeline:
    def process_item(self, item, spider):
        item['assets'] = self.process_assets(item['assets'], item['RPC'])
        return item

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
