package com.sentimentspark.sentimentsparkapp.model;

import java.util.ArrayList;
import java.util.List;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class CompaniesDTO {
    private final Boolean metaChecked;
    private final Boolean amazonChecked;
    private final Boolean netflixChecked;
    private final Boolean microsoftChecked;
    private final Boolean googleChecked;
    private final Boolean nvidiaChecked;
    private final Boolean teslaChecked;
    private final Boolean boeingChecked;

    public List<String> getAllChecked() {
        List<String> result = new ArrayList<>();
        if (Boolean.TRUE.equals(metaChecked)) result.add("META");
        if (Boolean.TRUE.equals(amazonChecked)) result.add("AMZN");
        if (Boolean.TRUE.equals(netflixChecked)) result.add("NFLX");
        if (Boolean.TRUE.equals(microsoftChecked)) result.add("MSFT");
        if (Boolean.TRUE.equals(googleChecked)) result.add("GOOG");
        if (Boolean.TRUE.equals(nvidiaChecked)) result.add("NVDA");
        if (Boolean.TRUE.equals(teslaChecked)) result.add("TSLA");
        if (Boolean.TRUE.equals(boeingChecked)) result.add("BA");

        return result;
    }
}
