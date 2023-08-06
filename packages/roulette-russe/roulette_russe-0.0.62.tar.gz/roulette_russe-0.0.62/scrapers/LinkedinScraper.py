from roulette_russe.Scraper import Scraper
from linkedin_api import Linkedin
from linkedin_api.utils.helpers import get_id_from_urn
from urllib.parse import urlencode

class LinkedinEnhanced(Linkedin):
    def __init__(self, username, password):
        super(LinkedinEnhanced, self).__init__(username=username, password=password)

    def get_company_employees(self, public_id):
        filters = ["resultType->PEOPLE","currentCompany->"+public_id]
        params = {"filters": "List({})".format(",".join(filters))}
        data = self.search(params, limit=1000)

        results = []
        for item in data:
            if "publicIdentifier" not in item:
                continue
            results.append('https://www.linkedin.com/in/'+get_id_from_urn(item.get("targetUrn")))
        return results

    def get_company_open_jobs(self, id):
        filters = [""]

    def search(self, params, limit=-1, offset=0):
        print('OOOOOOOK')
        """
        Do a search.
        """
        count = Linkedin._MAX_SEARCH_COUNT
        if limit is None:
            limit = -1

        results = []
        while True:
            # when we're close to the limit, only fetch what we need to
            if limit > -1 and limit - len(results) < count:
                count = limit - len(results)
            default_params = {
                "count": str(count),
                "filters": "List()",
                "origin": "OTHER",
                "q": "all",
                "start": len(results) + offset,
                "queryContext": "List()",
            }
            default_params.update(params)

            res = self._fetch(
                f"/search/blended?{urlencode(default_params, safe='(),')}",
                headers={"accept": "application/vnd.linkedin.normalized+json+2.1"},
            )
            data = res.json()

            new_elements = []
            elements = data.get("data", {}).get("elements", [])
            for i in range(len(elements)):
                new_elements.extend(elements[i]["elements"])
                # not entirely sure what extendedElements generally refers to - keyword search gives back a single job?
                # new_elements.extend(data["data"]["elements"][i]["extendedElements"])
            results.extend(new_elements)

            # break the loop if we're done searching
            # NOTE: we could also check for the `total` returned in the response.
            # This is in data["data"]["paging"]["total"]
            if (
                    (
                            limit > -1 and len(results) >= limit
                    )  # if our results exceed set limit
                    or len(results) / count >= Linkedin._MAX_REPEATED_REQUESTS
            ) or len(new_elements) == 0:
                break

            self.logger.debug(f"results grew to {len(results)}")

        return results


class LinkedinScraper(Scraper):
    def __init__(self, input_config, output_datasets, username, password, rr=None):
        super(LinkedinScraper, self).__init__(input_config, output_datasets, rr)
        self.api = LinkedinEnhanced(username, password)


    def query_company_details(self, account):
        company = self.api.get_company(account)
        return {
            "account": account,
            "company_name": company['name'],
            "tagline": company['tagline'],
            "description": company['description'],
            "company_industries": list(map(lambda x: x['localizedName'], company['companyIndustries'])),
            "company_specialities": company['specialities'],
            "company_headquarters": company['headquarter']['country'],
            "company_logo": company['logo']['image']['com.linkedin.common.VectorImage']['rootUrl'],
            "company_type": company['companyType']['code'],
            "company_followers": company['followingInfo']['followerCount'],
            "page_url": company['url'],
            "staff_count": company['staffCount']
        }

    def extract_company_updates(self, o):
        mentions = []
        if hasattr(o['value']['com.linkedin.voyager.feed.render.UpdateV2'], 'commentary'):
            if hasattr(o['value']['com.linkedin.voyager.feed.render.UpdateV2']['commentary']['text'], 'attributes'):
                mentions = list(map(lambda x: x['miniProfile']['publicIdentifier'],
                                    o['value']['com.linkedin.voyager.feed.render.UpdateV2']['commentary']['text'][
                                        'attributes']))
        return {
            "reactions":
                o['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts'][
                    'reactionTypeCounts'],
            "reactions_count":
                o['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts'][
                    'reactionTypeCounts'],
            "url": o['permalink'],
            "mentions": mentions,
            "comments_count":
                o['value']['com.linkedin.voyager.feed.render.UpdateV2']['socialDetail']['totalSocialActivityCounts'][
                    'numComments'],
            "id": o['id']
        }

    def query_company_updates(self, account):
        company_updates = self.api.get_company_updates(account)
        return list(map(lambda x : self.extract_company_updates(x), company_updates))

    def query_company_employees(self, account):
        employees = self.api.get_company_employees(account)
        return employees

    def scrap(self):
        tmp_list_profiles = []
        tmp_list_posts = []
        tmp_list_employees = []
        for account in self.input_config['accounts']:
            profile_data = self.query_company_details(account)
            tmp_list_profiles.append(profile_data)
        self.output_datasets['profiles'] = self.output_datasets['profiles'].append(tmp_list_profiles, ignore_index=True)
        if 'posts' in self.output_datasets:
            for account in self.input_config['accounts']:
                posts_data = self.query_company_updates(account)
                tmp_list_posts += list(posts_data)
            self.output_datasets['posts'] = self.output_datasets['posts'].append(tmp_list_posts, ignore_index=True)
        if 'employees' in self.output_datasets:
            for account in self.input_config['accounts']:
                employees_data = self.query_company_employees(account)
                tmp_list_employees.append({'account': account, 'followers': list(employees_data)})
            self.output_datasets['employees'] = self.output_datasets['employees'].append(tmp_list_employees,
                                                                                         ignore_index=True)

    def quality_check(self):
        pass
