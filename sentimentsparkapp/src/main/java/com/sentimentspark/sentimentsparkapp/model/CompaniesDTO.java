package com.sentimentspark.sentimentsparkapp.model;

import java.util.ArrayList;
import java.util.List;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class CompaniesDTO {
    private final Boolean metaChecked;
    private final Boolean amazonChecked;
    private final Boolean netflixChecked;

    public List<String> getAllChecked() {
        List<String> result = new ArrayList<>();
        if (Boolean.TRUE.equals(metaChecked)) result.add("META");
        if (Boolean.TRUE.equals(amazonChecked)) result.add("AMZN");
        if (Boolean.TRUE.equals(netflixChecked)) result.add("NFLX");

        System.out.println("LIST: " + result);
        return result;
    }
}
