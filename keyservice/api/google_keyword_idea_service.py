import json
import googleads
import pandas as pd
import traceback
from googleads import adwords
from googleads import oauth2


class SearchVolumePuller:
    def __init__(
        self, client_ID, client_secret, refresh_token, developer_token, client_customer_id,
    ):
        self.client_ID = client_ID
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.developer_token = developer_token
        self.client_customer_id = client_customer_id

    def get_client(self):
        access_token = oauth2.GoogleRefreshTokenClient(
            self.client_ID, self.client_secret, self.refresh_token
        )
        adwords_client = adwords.AdWordsClient(
            self.developer_token,
            access_token,
            client_customer_id=self.client_customer_id,
            cache=googleads.common.ZeepServiceProxy.NO_CACHE,
        )

        return adwords_client

    def get_service(self, service, client):

        return client.GetService(service)

    def get_target_ideas(self, service_client, keyword):
        data_list = list()
        PAGE_SIZE = 50
        selector = {"ideaType": "KEYWORD", "requestType": "IDEAS"}
        selector["requestedAttributeTypes"] = [
            "KEYWORD_TEXT",
            "COMPETITION",
            "SEARCH_VOLUME",
            "TARGETED_MONTHLY_SEARCHES",
        ]
        offset = 0
        selector["paging"] = {"startIndex": str(offset), "numberResults": str(PAGE_SIZE)}
        selector["searchParameters"] = [
            {"xsi_type": "RelatedToQuerySearchParameter", "queries": [keyword]}
        ]
        try:
            page = service_client.get(selector)
        except:
            page = None
        page = service_client.get(selector)
        if page:
            for result in page["entries"]:
                attributes = {}
                monthly_search = []
                for attribute in result["data"]:
                    attributes[attribute["key"]] = getattr(attribute["value"], "value", "0")
                for li in attributes["TARGETED_MONTHLY_SEARCHES"]:
                    month = {}
                    for k in li:
                        month[k] = li[k]
                    monthly_search.append(month)
                record = {
                    "keyword": attributes["KEYWORD_TEXT"],
                    "competition": attributes["COMPETITION"],
                    "search_volume": attributes["SEARCH_VOLUME"],
                    "monthly_search_volume": monthly_search,
                }
                data_list.append(record)
        else:
            print("error")
        return data_list

    @staticmethod
    def get_google_service(idea_key):
        CLIENT_ID = "748605680982-qerhgm1p3vh8tj93ij2kkam4ja7n9o0k.apps.googleusercontent.com"
        CLIENT_SECRET = "Ngd1x0xDHTwCpdRV3GxEwN1o"
        REFRESH_TOKEN = "1//0gviGgNh3hsIGCgYIARAAGBASNwF-L9IrtDkxPWbcMxtAG_xG-42qBSOoj-7PAk_x393-nz_3l7PbsMjoxxC_FHXOEqCzmf11ibs"
        DEVELOPER_TOKEN = "jtKXVf55IePS6-LWwpYvVA"
        CLIENT_CUSTOMER_ID = "683-841-0976"

        volume_puller = SearchVolumePuller(
            CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, DEVELOPER_TOKEN, CLIENT_CUSTOMER_ID
        )

        adwords_client = volume_puller.get_client()

        targeting_service = volume_puller.get_service("TargetingIdeaService", adwords_client)
        targeting_keyword_idea = volume_puller.get_target_ideas(targeting_service, idea_key)
        return targeting_keyword_idea


if __name__ == "__main__":
    CLIENT_ID = "748605680982-qerhgm1p3vh8tj93ij2kkam4ja7n9o0k.apps.googleusercontent.com"
    CLIENT_SECRET = "Ngd1x0xDHTwCpdRV3GxEwN1o"
    REFRESH_TOKEN = "1//0gviGgNh3hsIGCgYIARAAGBASNwF-L9IrtDkxPWbcMxtAG_xG-42qBSOoj-7PAk_x393-nz_3l7PbsMjoxxC_FHXOEqCzmf11ibs"
    DEVELOPER_TOKEN = "jtKXVf55IePS6-LWwpYvVA"
    CLIENT_CUSTOMER_ID = "683-841-0976"

    keyword_list = ["SEO", "Leeds", "Google"]

    volume_puller = SearchVolumePuller(
        CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, DEVELOPER_TOKEN, CLIENT_CUSTOMER_ID
    )

    adwords_client = volume_puller.get_client()

    targeting_service = volume_puller.get_service("TargetingIdeaService", adwords_client)

    # kw_sv_df = volume_puller.get_search_volume(targeting_service, keyword_list)
    # print(kw_sv_df)
    targeting_keyword_idea = volume_puller.get_target_ideas(targeting_service, "labtop")

