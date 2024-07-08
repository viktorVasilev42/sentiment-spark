document.addEventListener('DOMContentLoaded', (event) => {
    let stockStatsItems = document.getElementsByClassName("stocksStatsItem");
    var lastItem = stockStatsItems[stockStatsItems.length - 1];

    const checkHit = (item) => {
        if (parseInt(item.style.left, 10) <= -20) {
            let currLastLeft = parseFloat(lastItem.style.left, 10);
            item.style.left = (currLastLeft + 16) + "vw";
            lastItem = item;
        }
    }

    setInterval(() => {
        for (item of stockStatsItems) {
            let currLeft = parseFloat(item.style.left, 10);
            item.style.left = (currLeft - 0.1) + "vw";
            checkHit(item);
        }
    }, 10);


    let subPlotTitles = document.getElementsByClassName("subPlotTitle");
    for (title of subPlotTitles) {
        let currentString = title.innerHTML;
        if (currentString.includes("_")) {
            title.innerHTML = currentString.substring(0, currentString.indexOf("_"))
        }
    }
});

