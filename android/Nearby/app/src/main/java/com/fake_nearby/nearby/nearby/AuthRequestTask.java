package com.fake_nearby.nearby.nearby;

import android.os.AsyncTask;

import com.google.gson.JsonObject;

import java.io.IOException;
import java.util.List;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * Created by Lyn on 4/26/2016.
 */
public class AuthRequestTask extends AsyncTask<String, String, String>  {
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    public static final String baseUrl = "http://nearby.nick-jones.me/api";

    protected void onPreExecute() {
        // perhaps show a dialog
        // with a progress bar
        // to let your users know
        // something is happening
    }

    protected String doInBackground(String... aParams) {
        final OkHttpClient client = new OkHttpClient();
        JsonObject authJson = new JsonObject();
        authJson.addProperty("username", aParams[0]);
        authJson.addProperty("password", aParams[1]);
        System.out.println(aParams[0]);
        System.out.println(aParams[0]);

        RequestBody authBody = RequestBody.create(JSON, authJson.toString());
        Request request = new Request.Builder().url(baseUrl + "/access").post(authBody).build();
        System.out.println(request.toString());
        try {
            Response response = client.newCall(request).execute();
            System.out.println(response.toString());
            return response.toString();
        }
        catch (IOException e) {
            System.out.println("Bad api call");
            return "";
        }
    }

    protected void onPostExecute(String token) {
        // background work is finished,
        // we can update the UI here
        // including removing the dialog
    }
}
