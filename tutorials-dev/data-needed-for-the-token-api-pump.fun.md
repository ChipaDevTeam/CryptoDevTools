curl example to get trades: - DONE

```
curl ^"https://swap-api.pump.fun/v2/coins/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump/trades?limit=100^&cursor=0^&minSolAmount=0^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"c96c-7/XDf6sjhhVOHCEvY8y5p6Ts4Q0^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

latest token:

```
curl ^"https://frontend-api-v3.pump.fun/coins/latest^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"534-HkbpUzPxQFzgXhxZ7DzN6CWmJbw^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```


Specific token info:

```
curl ^"https://frontend-api-v3.pump.fun/coins/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"72b-y/ZPuvJR6Ag36V+aB9izWgnS8uU^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

Batch all time highs:

```
curl ^"https://swap-api.pump.fun/v1/coins/ath/batch^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"content-type: application/json^" ^
  -b ^"_ga=GA1.1.1573348401.1758044772; intercom-id-w7scljv7=55144242-72a2-406e-b6a9-69e02f966a6f; intercom-session-w7scljv7=; intercom-device-id-w7scljv7=6372a7fc-02ed-485a-b211-086b928421a8; __cf_bm=iezLzaoHl5SIW7.mqFufvZrDDgspDeLTd1yqymO8c.A-1758118282-1.0.1.1-cgwPp5DivMzzTNBYeI4Yu0YDcKxQgrdafuYmXMTRWohZnR_PQfp0feenVi_Jalx8d8D9wgwZ4dM8XJxMKWpAk_Gdh4NmpVDxs.ya9c8e1Io; _cfuvid=NxrjvP8WUlLKl.ANW4TMgXApeUMET_ZO3oJGjDvhmN8-1758118282152-0.0.1.1-604800000; _ga_T65NVS2TQ6=GS2.1.s1758118305^$o4^$g0^$t1758118305^$j60^$l0^$h0; cf_clearance=3EmqBIivfbdwewXuqO_L3cLjMc4XG1sXKwoSE53pkYI-1758118307-1.2.1.1-qxiiqm4pT.uamoxuAKp68yHWRY_6XiXpEC3gIQkxxvCxraHViKE1_pTt24BAkVbkCbF5tkRnX8hl6dXamvGiV_I79tIno6O1UbYgCmk5LPhdTwKrrNSJhFOx14O8qcp.Zbi_Fnowq1CJZTSBNqmPxNu0PXvCvw5AmjTYeIvRxHDVlomK38QN9g8B0_.jRS.JOawV7CxFQYtCEVPfYJOEbp9KEh1hCUhPtdrEeyqroBE^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^" ^
  --data-raw ^"^{^\^"addresses^\^":^[^\^"HKSRu2zoAyiB29UDvTZ3oxKbyoFbVLaYGthoWZAbBaVr^\^",^\^"HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump^\^"^],^\^"currency^\^":^\^"USD^\^"^}^"
```

pool specific:

```
curl ^"https://swap-api.pump.fun/v1/pools/AzkPsCQBYwmM4m2mXvjMcAW6aJJqBSzaVFz1YuvcqrHe/ath?currency=USD^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"23-wIwZHVO7JEdZJrvbPMecMJE6g7g^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

all time volume:

```
curl ^"https://swap-api.pump.fun/v1/coins/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump/all-time-volume?currency=USD^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"21-4Abd5W42EPsbj/EDNoltdDPOQ9E^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

market activity:

```
curl ^"https://swap-api.pump.fun/v1/pools/AzkPsCQBYwmM4m2mXvjMcAW6aJJqBSzaVFz1YuvcqrHe/market-activity^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"371-09GxVy41PHuxtxlOTOpdBNPW0jE^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

Snipper count:

```
curl ^"https://swap-api.pump.fun/v1/coins/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump/sniper-count^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"d2e-Sug0Pr1ODqaDAzdMSOGuDgfNWEc^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

sol price:

```
curl ^"https://frontend-api-v3.pump.fun/sol-price^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"13-KoYUVdHDO7EUkA0oVIVDkA/FsGY^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```

Get Candles:

```
curl ^"https://swap-api.pump.fun/v2/coins/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump/candles?interval=1m^&limit=1000^&currency=USD^&createdTs=1758058204557^" ^
  -H ^"accept: */*^" ^
  -H ^"accept-language: en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5^" ^
  -H ^"if-none-match: W/^\^"58c-ooSplb+yvPX+Q0yPIF+kZQT5wDg^\^"^" ^
  -H ^"origin: https://pump.fun^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"sec-ch-ua: ^\^"Opera GX^\^";v=^\^"121^\^", ^\^"Chromium^\^";v=^\^"137^\^", ^\^"Not/A)Brand^\^";v=^\^"24^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0^"
```
