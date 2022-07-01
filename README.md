# api-newstool

This code takes a serie of parameters and output news in a structured format (JSON). The code is hosted on Heroku using Flask server.

To run it, you can visit https://api-newstool.herokuapp.com/ to activate the dynos. The program has initialised once you get a response "Running!".

## Parameters

To put a job into queue you can make a GET resquest with the following parameters:

```json
{
    "input": {
        "keywords": [
            "Elon Musk",
            "Tesla"
        ],
        "kwargs": {
            "countries": null,
            "labels": null,
            "languages": null,
            "limit": null,
            "ner": false,
            "rank": false,
            "weak": true
        },
        "timeframe": "7d",
        "translate_search": false,
        "translate_title": true
    }
```

### Timeframe
The format of the timeframe is a string comprised of a number, followed by a letter representing the time operator. For example 1y would signify 1 year. Full list of operators below:

 - h = hours (eg: 12h)
 - d = days (eg: 7d)
 - m = months (eg: 6m)
 - y = years (eg: 1y)

### Languages and Countries
The languages or countries to source the articles from.

1. NOTE THAT YOU CAN NOT USE LANGUAGES AND COUNTRIES IN THE SAME SEARCH
2. You can provide a list of languages to search the articles. These can be input similarly to keywords, that is, 
   without using space between the languages code.
3. The list of the languages and countries accepted can be found below:

```
AVAILABLE_COUNTRIES = {‘Australia': 'AU', 'Botswana': 'BW', 'Canada ': 'CA', 'Ethiopia': 'ET', 'Ghana': 'GH', 'India ': 'IN',
 'Indonesia': 'ID', 'Ireland': 'IE', 'Israel ': 'IL', 'Kenya': 'KE', 'Latvia': 'LV', 'Malaysia': 'MY', 'Namibia': 'NA',
 'New Zealand': 'NZ', 'Nigeria': 'NG', 'Pakistan': 'PK', 'Philippines': 'PH', 'Singapore': 'SG', 'South Africa': 'ZA',
 'Tanzania': 'TZ', 'Uganda': 'UG', 'United Kingdom': 'GB', 'United States': 'US', 'Zimbabwe': 'ZW',
 'Czech Republic': 'CZ', 'Germany': 'DE', 'Austria': 'AT', 'Switzerland': 'CH', 'Argentina': 'AR', 'Chile': 'CL',
 'Colombia': 'CO', 'Cuba': 'CU', 'Mexico': 'MX', 'Peru': 'PE', 'Venezuela': 'VE', 'Belgium ': 'BE', 'France': 'FR',
 'Morocco': 'MA', 'Senegal': 'SN', 'Italy': 'IT', 'Lithuania': 'LT', 'Hungary': 'HU', 'Netherlands': 'NL',
 'Norway': 'NO', 'Poland': 'PL', 'Brazil': 'BR', 'Portugal': 'PT', 'Romania': 'RO', 'Slovakia': 'SK', 'Slovenia': 'SI',
 'Sweden': 'SE', 'Vietnam': 'VN', 'Turkey': 'TR', 'Greece': 'GR', 'Bulgaria': 'BG', 'Russia': 'RU', 'Ukraine ': 'UA',
 'Serbia': 'RS', 'United Arab Emirates': 'AE', 'Saudi Arabia': 'SA', 'Lebanon': 'LB', 'Egypt': 'EG',
 'Bangladesh': 'BD', 'Thailand': 'TH', 'China': 'CN', 'Taiwan': 'TW', 'Hong Kong': 'HK', 'Japan': 'JP',
 'Republic of Korea': 'KR'}

AVAILABLE_LANGUAGES = {‘english': 'en', 'indonesian': 'id', 'czech': 'cs', 'german': 'de', 'spanish': 'es-419', 'french': 'fr',
 'italian': 'it', 'latvian': 'lv', 'lithuanian': 'lt', 'hungarian': 'hu', 'dutch': 'nl', 'norwegian': 'no',
 'polish': 'pl', 'portuguese brasil': 'pt-419', 'portuguese portugal': 'pt-150', 'romanian': 'ro', 'slovak': 'sk',
 'slovenian': 'sl', 'swedish': 'sv', 'vietnamese': 'vi', 'turkish': 'tr', 'greek': 'el', 'bulgarian': 'bg',
 'russian': 'ru', 'serbian': 'sr', 'ukrainian': 'uk', 'hebrew': 'he', 'arabic': 'ar', 'marathi': 'mr', 'hindi': 'hi',
 'bengali': 'bn', 'tamil': 'ta', 'telugu': 'te', 'malyalam': 'ml', 'thai': 'th', 'chinese simplified': 'zh-Hans',
 'chinese traditional': 'zh-Hant', 'japanese': 'ja', 'korean': 'ko'}
```

### Translate title
1. This parameter is used to determine whether you want to translate the title of the articles in English. 
   This can be particularly useful if you’re looking for articles in a language that you’re not confortable with.
2. THIS SHOULD BE True IF YOU ATTEMPT CLASSIFICATION WITH THE LABELS FIELD


### Translate search
Combining with languages if provided, this paranmeter is particularly useful for translating the keywords in multiple languages. For example, if you want to search 3d printing in French and English, turning this to true this will automatically change the 3d printing to “impression 3d” for the French articles.

### Labels, Named entity Recognition & Rank
These use huggingface pipeline to classify by a list of classes (Labels), perform NER and rank result by relevance. Because the hosting platform (Heroku) is on the free plan, passing any of these will trigger memory overflow of the worker dyno due to the memmory needs of the Machine Learning algorithms.

## Make a Request

to make a request you need to construct a URL using /enqueue/. un example of a request for the articles on Bitcoin & Ethereum for today is:
https://api-newstool.herokuapp.com/enqueue/?keywords=ethereum&keywords=bitcoin&timeframe=1d&translate_title=True&translate_search=False

When this is searched the program will return you a job id:

```json
{
"job_id": "495c9c17-b0b3-4d12-ae99-e47fd5a38b6d"
}
```

You can copy paste the job id and check the status of the request using /check_status like so:
https://api-newstool.herokuapp.com/check_status?job_id=495c9c17-b0b3-4d12-ae99-e47fd5a38b6d

This returns information about the process' states:

```json
{
"job_id": "495c9c17-b0b3-4d12-ae99-e47fd5a38b6d",
"job_status": "started"
}


wait for it to turn to ->

{
"job_id": "495c9c17-b0b3-4d12-ae99-e47fd5a38b6d",
"job_status": "finished"
}
```

Once the job has finished you can view the results here using /get_result (the json is available for 500 seconds):
https://api-newstool.herokuapp.com/get_result?job_id=495c9c17-b0b3-4d12-ae99-e47fd5a38b6d

### Sample Output 

Both bitcoin and ethereum returned the max amount of articles each in the last day (100)

```json
{
  "input": {
    "keywords": [
      "ethereum",
      "bitcoin"
    ],
    "kwargs": {
      "countries": null,
      "labels": null,
      "languages": null,
      "limit": null,
      "ner": false,
      "rank": false,
      "weak": true
    },
    "timeframe": "1d",
    "translate_search": false,
    "translate_title": true
  },
  "job_enqueued_at": "2022-07-01T10:18:15.280018",
  "job_id": "495c9c17-b0b3-4d12-ae99-e47fd5a38b6d",
  "job_started_at": "2022-07-01T10:18:15.317387",
  "result": [
    {
      "content": "",
      "href": "https://www.analyticsinsight.net",
      "image": "",
      "keyword": "ethereum",
      "published date": "Fri, 01 Jul 2022 04:56:08 GMT",
      "publisher": "Analytics Insight",
      "summary": "",
      "timeframe": "1d",
      "title": "Ethereum Rally is Possible Only if ETH Crosses US$1,500 Resistance - Analytics Insight",
      "url": "https://www.analyticsinsight.net/ethereum-rally-is-possible-only-if-eth-crosses-us1500-resistance/"
    },
    {
      "content": "Editorial Independence We want to help you make more informed decisions. Some links on this page — clearly marked — may take you to a partner website and may result in us earning a referral commission. For more information, see How We Make Money.\n\nAfter a brief spike earlier this week, cryptocurrency prices came back down Thursday.\n\nSeveral experts we talked to said the prices would likely fall again despite the upward trend, as pressure continues to mount from macroeconomic uncertainty and a liquidity crisis among crypto firms.\n\nAnd that’s exactly what happened.\n\nBitcoin fell below $20,000 on Thursday, a near 8% drop over the last seven days. Ethereum experienced a big drop too, falling to nearly $1,000. The largest crypto is down more than 70% from last year’s all-time high of $68,000.\n\nVolatility is par for the course for crypto, and while bitcoin has fallen below the key support level of $20,000, it could easily bounce back up. For investors, a big question still lingers: Is the crypto market on its way to recovery or is it just another false alarm, also known as a bull trap?\n\nSome experts say signs point to a bull trap and investors should be wary, warning the worst may be yet to come amid ongoing macroeconomic uncertainty — and bitcoin’s price, as well as other cryptocurrencies, could drop even further.\n\n“While we have seen bitcoin and ethereum rally recently after creating lows around $17,500 and $880 respectively, we are unconvinced about calling a low in place yet,” says Richard Usher, head of over-the-counter trading at BCB Group, a crypto financial firm. “The general risk environment remains on a knife edge, and while we think risk assets will rally significantly toward the end of the year, we see risks skewed to one more sell-off first.”\n\nIs the Crypto Market Recovering or Just a Bull Trap?\n\nIt’s easy for investors to hope the worst is in the past for the crypto market. Bitcoin’s price stayed above $20,000 and ethereum held above $1,100 on Tuesday, a significant jump from their 15-month lows just two weeks ago.\n\nBut with war raging in Ukraine, rising interest rates, inflation soaring, and talks of an impending recession, the coast is far from clear, experts say. Many are calling what we’re seeing with crypto prices this week a bull trap.\n\nThat’s when a stock or cryptocurrency reverses back down after a convincing rally and breaks below a prior support level. Basically, it’s a false signal, fooling investors into thinking the market is done falling and that it’s a good time to buy.\n\nExperts say there will likely be another sell-off in the crypto market over the next few weeks or months. Wendy O, a crypto expert and educator, expects ethereum could fall as low as $750 and bitcoin could fall to $10,000. Kiana Danial, entrepreneur and author of “Cryptocurrency Investing for Dummies,” predicts bitcoin will fall to $11,000, while venture capitalist Kavita Gupta is calling for a bottom of $14,000 for bitcoin and $500 for ethereum.\n\nMartin Hiesboeck, head of blockchain and crypto research at Uphold, says whether bitcoin holds above $20,000 has little to do with crypto itself and more with the overall geopolitical and macroeconomic situation, which he does not believe will improve significantly in the short term. The crypto market, which has been tracking with the stock markets lately, has been a casualty of the broader market sell-off of risky assets.\n\n“The war in Ukraine, supply chain gluts, and inflation are by far the biggest worries,” Hiesboeck says. “So far bitcoin hasn’t exactly proven to be the inflation-proof safe haven it’s biggest fans believed it to be.”\n\nIs It a Good Time to Invest in Crypto?\n\nThe crypto market is volatile and highly unpredictable, so buying cryptocurrencies at any price is risky — let alone during a market dip that might not go away anytime soon.\n\nHowever, if you’ve assessed your tolerance and can accept the risk, experts say now could be a good time to get in the crypto market since prices are lower than they’ve been in years. There’s no such thing as a “perfect” time to enter the market, so keep in mind that price fluctuations are par for the course and be prepared for crypto prices to fall even more. Don’t invest in crypto if you can’t stomach sharp market swings, which can sometimes be as much as 15% in a 24-hour period.\n\nAdditionally, you should invest only what you’re OK with losing and after you’ve prioritized other aspects of your finances, such as building an emergency fund, paying off high-interest debt, and investing in a traditional retirement account like a 401(k).\n\nFinancial advisors recommend investing no more than 5% of your portfolio in crypto, and sticking to the two most well-established cryptocurrencies: bitcoin and ethereum. According to the NextAdvisor Investability Score, bitcoin and ethereum are considered to be better investments thanks to their longer track records and long-term value growth, among other key factors. Here’s how our score shakes out for 10 cryptocurrencies that are consistently among the top by market cap, excluding stablecoins, for reference:",
      "href": "https://time.com",
      "image": "https://time.com/nextadvisor/wp-content/uploads/2022/06/Bitcoin-and-Ethereum-Rallied-This-Week-Heres-Why-It-May-Not-Last-According-to-Experts-1000x630.jpg",
      "keyword": "ethereum",
      "published date": "Thu, 30 Jun 2022 14:26:15 GMT",
      "publisher": "NextAdvisor",
      "summary": "But with war raging in Ukraine, rising interest rates, inflation soaring, and talks of an impending recession, the coast is far from clear, experts say.\nMany are calling what we’re seeing with crypto prices this week a bull trap.\nExperts say there will likely be another sell-off in the crypto market over the next few weeks or months.\nWendy O, a crypto expert and educator, expects ethereum could fall as low as $750 and bitcoin could fall to $10,000.\nThe crypto market, which has been tracking with the stock markets lately, has been a casualty of the broader market sell-off of risky assets.",
      "timeframe": "1d",
      "title": "After a Short Rally, Bitcoin and Ethereum Prices Plummet. Here’s What Comes Next, According to These Experts - NextAdvisor",
      "url": "https://time.com/nextadvisor/investing/cryptocurrency/bitcoin-ethereum-prices-rise-crypto-bull-trap/"
    },
    {
      "content": "It’s another day, another upgrade for Ethereum as the world’s largest smart contracts platform has just rolled out a new major update.\n\nCalled “Gray Glacier,” the upgrade occurred at block 15,050,000 on June 30 with the sole goal of introducing changes to the parameters of the network’s difficulty bomb, pushing it back by 700,000 blocks, or roughly 100 days.\n\nThe Gray Glacier upgrade is the network’s hard fork, which means it is creating new rules to improve the system and requires the node operators and miners to download the latest version of their Ethereum clients.\n\n“If you are using an Ethereum client that is not updated to the latest version, […] your client will sync to the pre-fork blockchain once the upgrade occurs,” the Ethereum Foundation said in a blog post earlier this month.\n\nIn other words, the non-upgraded clients are stuck on an incompatible chain following the old rules, meaning that operators won’t be able to send transactions or operate on the post-upgrade Ethereum network.\n\nWhat's more, not all node operators and miners followed the recommendation though, as data from Ethernodes shows that only 65% of clients were fully prepared for the Gray Glacier upgrade.\n\nErigon, the network’s second-largest client, was the only one to have all of its 164 clients upgraded.\n\nGeth, the network’s most popular client, was only 67% ready, with as many as 448 clients running the outdated software. Nethermind and Besu had 76% and 78% of its clients updated, respectively.\n\nWhat is Ethereum's difficulty bomb?\n\nThe difficulty bomb, which has been a part of Ethereum since day one, is a piece of code responsible for exponentially increasing the difficulty of mining Ethereum (ETH), the network’s native cryptocurrency, and thus disincentivizing miners to continue their operations as the network transitions from its current proof-of-work (PoW) algorithm to proof-of-stake (PoS) consensus model.\n\nIn other words, detonating the difficulty bomb would mean that the actual transition—otherwise known as The Merge—could be just around the corner.\n\nAn implementation of The Merge has already gone live on Ethereum’s Ropsten testnet at the beginning of June, with Vitalik Buterin and other developers previously saying that ”if everything goes to plan,\" the transition could happen as early as August this year.\n\nPushing back the difficulty bomb for another 100 days, however, makes it unlikely that the schedule will be met, with the updated EIP-5133 proposal now pointing to mid-September as a new time frame for the implementation of the mechanism.\n\nPreviously, the difficulty bomb mechanism has been pushed back in five different network upgrades: Byzantium, Constantinople, Muir Glacier, London, and the most recent Arrow Glacier upgrade in December 2021.",
      "href": "https://decrypt.co",
      "image": "https://cdn.decrypt.co/resize/1024/height/512/wp-content/uploads/2022/04/ethereum-gID_6.jpg",
      "keyword": "ethereum",
      "published date": "Thu, 30 Jun 2022 11:26:29 GMT",
      "publisher": "Decrypt",
      "summary": "It’s another day, another upgrade for Ethereum as the world’s largest smart contracts platform has just rolled out a new major update.\nCalled “Gray Glacier,” the upgrade occurred at block 15,050,000 on June 30 with the sole goal of introducing changes to the parameters of the network’s difficulty bomb, pushing it back by 700,000 blocks, or roughly 100 days.\nThe Gray Glacier upgrade is the network’s hard fork, which means it is creating new rules to improve the system and requires the node operators and miners to download the latest version of their Ethereum clients.\nIn other words, detonating the difficulty bomb would mean that the actual transition—otherwise known as The Merge—could be just around the corner.\nPreviously, the difficulty bomb mechanism has been pushed back in five different network upgrades: Byzantium, Constantinople, Muir Glacier, London, and the most recent Arrow Glacier upgrade in December 2021.",
      "timeframe": "1d",
      "title": "‘Gray Glacier’ Upgrade Goes Live on Ethereum Network - Decrypt",
      "url": "https://decrypt.co/104065/gray-glacier-upgrade-goes-live-ethereum-network"
    }
  ]
}






