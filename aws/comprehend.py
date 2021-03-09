import collections

from aws import get_aws_client


def process_text(text_list: list):
    comp_client = get_aws_client("comprehend")
    sentiment_results = comp_client.batch_detect_sentiment(TextList=text_list, LanguageCode="en")["ResultList"]

    for sr in sentiment_results:
        sr["Text"] = text_list[sr["Index"]]

    final_sentiment = _process_results(sentiment_results)
    return {"final_sentiment": final_sentiment, "comprehend_data": sentiment_results}


def _process_results(results: list) -> str:
    cntr = collections.Counter([l["Sentiment"] for l in results if l["Sentiment"] in ("POSITIVE", "NEGATIVE", "MIXED")])
    return cntr.most_common(1)[0][0]
