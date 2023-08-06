#### A package for the Taromaru API.


##### Image Example (no async):

```py
    from taromaru import taromaru

    taromaru = taromaru("YOUR API KEY HERE")

    results = taromaru.image(type="kanna")

    print(results)
```

##### Image Example (async):

```py
    from taromaru import taromaruasync
    import asyncio

    taromaru = taromaruasync("YOUR API KEY HERE")

    results = asyncio.get_event_loop().run_until_complete(taromaru.image(type="kanna"))

    print(results)
```

[API Location](https://taromaruapi.cu.ma)