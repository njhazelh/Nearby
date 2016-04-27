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

    public static void doDisplayNameRequest() {

    }

    public static void doAuthRequest(String username, String password) {
        System.out.println(ApiRequests.authToken);
        new AuthRequestTask().execute(username, password);
        System.out.println(ApiRequests.authToken);
    }
}
