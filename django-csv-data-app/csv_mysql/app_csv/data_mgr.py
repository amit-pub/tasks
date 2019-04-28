from datetime import datetime
import json

from django.db.models import Sum, FloatField, F
import django.core.exceptions as DjangoErrors
from .models import CsvRow


# Declaration of few Macros to make them scalable with min changes
OPERATORS = ["lte", "lt", "gt", "gte"]

KEYS = ["date","channel","country","os","impressions",
        "installs","clicks","spend","revenue"]

SUBKEYS = ["month", "year", "day"]


# this is the only one Annotator for which code has been implemented, but it
# can easily be changed to support more such annotations,
# basically idea is to have mapping of the string-keyword with module-reference
ANNOTATORS = {"Sum": Sum}


class DataManager():
    def __init__(self):
        pass

    def get_data(self, query):
        final_res = {}
        if query:
            # if there is query requested, prepare the query in req'd format
            query_dict = self._prepare_query(query)

            # fething filtering patterns and functions from prepared-query
            order_by = query_dict.get("order_by")
            values = query_dict.get("values")
            annotator = query_dict.get("annotator")
            filters = query_dict.get("filters")
 
            try:

                # as each of below steps is to make sure all the requested
                # filtering, sorting, annotating is to be applied,
                # applying it in the part, since the actual data gathering
                # happens only when we read the data using cursor of model

                records = CsvRow.objects.filter(**filters)
                if order_by:
                    records = records.order_by(*order_by)

                if values and annotator:
                    records = records.values(*values).annotate(**annotator)
                elif annotator:
                    records = records.annotate(**annotator)
                elif values:
                    records = records.values(*values)

            except DjangoErrors.FieldError as e:
                print e
                raise Exception("Invalid field in request")
        else:
            # TODO: we can add Pagination here
            # user can have a provision of pagination by specifying values:
            # start_from, limit in URL options
            records = CsvRow.objects.filter()


        """
        below is the output/result formatting code, which can be easily
        factored into creating a new method, here since there isn't any
        other consumer, keeping it as is.
        """

        # convert the type to listing, as to make it JSON Serializable
        result = list(records)

        # get the count of records before outputting actual items
        final_res["count"] = records.count()

        # fill the items( the actual user requested data) in all possible cases
        if not result:
            final_res["items"] = []
        elif isinstance(type(result[0]), dict):
            final_res["items"] = [result]
        else:
            # the output would have records of model.CsvRow, hence call INFO
            # to get the user-required data in user-desired format.
            # as per the requirement, models.CsvRow.info() method can be
            # changed to have the data formatted uniformly across all results
            if hasattr(result[0], "info"):
                final_res["items"] = [i.info() for i in result]
            else:
                final_res["items"] = result

        return final_res


    def _prepare_query(self, query):
        # this method helps in identifying the query format & validating them
        # and formatting them in required backend format
        kwargs = {}
        order_by = []
        values = []
        annotators = {}
        if not query.get("query"):
            raise Exception("Invalid query request")

        # take one condition at-a-time from the list of queries
        for cond in query["query"][0].split(","):
            k, v = cond.split("=")
            op = None
            # list type values aren't required, so type-cast it 
            # by using its only value
            if isinstance(v, list):
                v = v[0]

            # below few if blocks are to handle specific keyword cases,
            # such as ANNOTATORS, sort_by, values, order_by

            if k in ANNOTATORS.keys():
                annotators[v]=ANNOTATORS[k](v)
                continue

            if k == "sort_by":
                order_by.append(v)
                continue

            if k == "values":
                values.extend(v.split(","))
                continue

            if k not in KEYS:
                if k not in SUBKEYS:
                    raise Exception("Invalid field '%s' requested" % k)
                else:
                    # this is one of subkeys
                    k = "date__%s" % k

            # here, ":" is used to specify the [lte, gte, le, ge] conditions
            if ":" in v:
                op, v = v.split(":")
                if op not in OPERATORS:
                    raise Exception("Unsupported operator")

                k = k + "__" + op if op else k

            # have separate handling for "date" key, since converison is req'd
            if k == "date":
                try:
                    v = datetime.strptime(v, "%Y-%m-%d")
                except Exception as e:
                    print e
                    raise Exception("Please check datetime format." \
                                    "Supported format is: %Y-%m-%d")
            kwargs[k] = v

        return {"filters": kwargs, "order_by": order_by, "values": values,
                "annotator": annotators}


    def get_cpi(self, query):
        query_dict = self._prepare_query(query)
        filters = query_dict["filters"]
        if not filters:
            filters = {"country": "CA"}

        # get filtered values with output-ing "channel"
        temp = CsvRow.objects.filter(**filters).values("channel")

        # get the expenditure values and assign alias to them
        temp = temp.annotate(total_spend=Sum("spend",
                                             output_field=FloatField()),
                             total_installs=Sum("installs",
                                                output_field=FloatField()))

        # Get the Cost-per-install by doing division of above calculated totals
        result = temp.annotate(cpi=F("total_spend")/F("total_installs"))

        return list(result)
