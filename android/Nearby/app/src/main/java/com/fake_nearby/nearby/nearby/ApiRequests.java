package com.fake_nearby.nearby.nearby;


import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by Lyn on 4/26/2016.
 */
public class ApiRequests {

    public static String authToken = "";
    public static final String baseUrl = "http://nearby.nick-jones.me/api";
    private final Gson gson = new Gson();
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    public static void reportObservation(String timestamp, String mac, int rssi) {
        if (!authToken.equals("")) {
            new ReportObservationTask().execute(timestamp, mac, Integer.toString(rssi));
        }
    }

    public static void addDevice(String mac) {
        if (!authToken.equals("")) {
            new AddDeviceTask().execute(mac);
        }
    }

    public static void doAuthRequest(String username, String password) {
        new AuthRequestTask().execute(username, password);
        System.out.println(ApiRequests.authToken);
    }

    public static void createAccount(String username, String password, String fullname) {
        String[] name = fullname.split("\\s+");
        new CreateAcctTask().execute(username, password, name[0], name[1]);
    }
}
