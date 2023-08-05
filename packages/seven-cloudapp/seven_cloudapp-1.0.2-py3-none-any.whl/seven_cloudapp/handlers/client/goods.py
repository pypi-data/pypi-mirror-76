# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-28 14:50:27
@LastEditTime: 2020-08-07 09:35:14
@LastEditors: HuangJingCan
@Description: 
"""

from handlers.seven_base import *
from models.db_models.prize.prize_roster_model import *
from models.db_models.act.act_prize_model import *
from models.db_models.app.app_info_model import *

from models.top_model import *


class SubmitSkuHandler(SevenBaseHandler):
    """
    @description: 提交SKU
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    @filter_check_params("sku_id")
    def get_async(self):
        app_id = self.get_taobao_param().source_app_id
        open_id = self.get_taobao_param().open_id

        user_prize_id = int(self.get_param("user_prize_id"))
        properties_name = self.get_param("properties_name")
        sku_id = self.get_param("sku_id")

        prize_roster_model = PrizeRosterModel()
        prize_roster = prize_roster_model.get_entity("id=%s", params=user_prize_id)
        if not prize_roster:
            return self.reponse_json_error("NoUserPrize", "对不起，找不到该奖品")
        if prize_roster.is_sku > 0:
            goods_code_list = json.loads(prize_roster.goods_code_list)
            goods_codes = [i for i in goods_code_list if str(i["sku_id"]) == sku_id]

            prize_roster.sku_id = sku_id
            prize_roster.properties_name = properties_name
            if goods_codes and ("goods_code" in goods_codes[0].keys()):
                prize_roster.goods_code = goods_codes[0]["goods_code"]

        prize_roster_model.update_entity(prize_roster)

        self.reponse_json_success()


class SkuInfoHandler(SevenBaseHandler):
    """
    @description: 获取SKU信息
    @param {type} 
    @return: 
    @last_editors: CaiYouBin
    """
    def get_async(self):
        num_iids = self.get_param("num_iids")

        if self.get_param("source_app_id") == config.get_value("client_template_id"):
            sku_info = self.get_sku_info2()
            return self.reponse_json_success(sku_info)

        access_token = ""
        app_info = AppInfoModel().get_entity("app_id=%s", params=self.get_taobao_param().source_app_id)
        if app_info:
            access_token = app_info.access_token

        rep_dic = TopModel().get_sku_info(num_iids, access_token)
        self.reponse_custom(rep_dic)

    def get_sku_info2(self):
        sku_info = {
            "items": {
                "item": [{
                    "input_str": "984055037,棉95% 聚氨酯弹性纤维(氨纶)5%,粉色-女款;颜色分类;黄色-男款",
                    "nick": "阪织屋旗舰店",
                    "num_iid": 615956945446,
                    "pic_url": "https://img.alicdn.com/bao/uploaded/i3/2089529736/O1CN01GdsGYs2Ln8i0Dxv3c_!!0-item_pic.jpg",
                    "property_alias": "",
                    "props_name":
                    "20000:223946830:品牌:阪织屋;20021:105255:面料主材质:棉;20509:28314:尺码:S;20509:28315:尺码:M;20509:28316:尺码:L;20509:28317:尺码:XL;20603:14031880:图案:卡通动漫;20608:31755:家居服风格:卡通;24477:47698:适用性别:情侣;31745:3500872:件数:2件;1627207:380784160:颜色分类:粉色-女款;1627207:15039988:颜色分类:黄色-男款;8560225:828918270:上市时间:2020年夏季;13021751:7837058106:款号:984055037;13328588:493262620:成分含量:81%(含)-95%(含);122216507:3216783:厚薄:薄款;122216515:4060838:适用场景:休闲家居;122216608:3267959:适用对象:青年;148380063:852538341:销售渠道类型:纯电商(只在线上销售);149422948:854658283:面料材质成分:棉95% 聚氨酯弹性纤维(氨纶)5%",
                    "skus": {
                        "sku": [{
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372101",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28314",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28314:尺码:S",
                            "quantity": 28,
                            "sku_id": 4511701590232
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372102",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28315",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28315:尺码:M",
                            "quantity": 73,
                            "sku_id": 4511701590233
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550372103",
                            "price": "329.00",
                            "properties": "1627207:380784160;20509:28316",
                            "properties_name": "1627207:380784160:颜色分类:粉色-女款;20509:28316:尺码:L",
                            "quantity": 71,
                            "sku_id": 4511701590234
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384002",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28315",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28315:尺码:M",
                            "quantity": 0,
                            "sku_id": 4511701590235
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384003",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28316",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28316:尺码:L",
                            "quantity": 53,
                            "sku_id": 4511701590236
                        }, {
                            "created": "2020-04-14 16:21:58",
                            "modified": "2020-06-21 00:07:43",
                            "outer_id": "9840550384004",
                            "price": "369.00",
                            "properties": "1627207:15039988;20509:28317",
                            "properties_name": "1627207:15039988:颜色分类:黄色-男款;20509:28317:尺码:XL",
                            "quantity": 23,
                            "sku_id": 4511701590237
                        }]
                    },
                    "title": "阪织屋睡衣女迪士尼情侣睡衣米老鼠棉质印花女士短袖短裤套头套装"
                }]
            }
        }
        return sku_info