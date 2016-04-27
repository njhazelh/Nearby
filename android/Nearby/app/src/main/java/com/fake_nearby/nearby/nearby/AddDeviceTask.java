package com.fake_nearby.nearby.nearby;

import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.preference.PreferenceActivity;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

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
public class AddDeviceTask extends AsyncTask<String, Boolean, Boolean>  {
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    public static final String baseUrl = "http://nearby.nick-jones.me/api";

    protected void onPreExecute() {
        // perhaps show a dialog
        // with a progress bar
        // to let your users know
        // something is happening
    }

    protected Boolean doInBackground(String... aParams) {
        final OkHttpClient client = new OkHttpClient();
        final Gson gson = new Gson();
        JsonObject addDevice = new JsonObject();
        addDevice.addProperty("mac", aParams[0]);
        System.out.println(aParams[0]);

        RequestBody authBody = RequestBody.create(JSON, addDevice.toString());
        Request request = new Request.Builder().url(baseUrl + "/devices").post(authBody).addHeader("Authentication", aParams[1]).build();
        try {
            Response response = client.newCall(request).execute();
            if (response.code() == 200) {
                JsonParser parser = new JsonParser();
                JsonElement element = parser.parse(response.body().string());
                JsonObject jsonObject = element.getAsJsonObject();
                System.out.println(jsonObject.get("message").getAsString());
                return true;
            }
            else {
                System.out.println("Bad http response: add device " + response.code());
                return false;
            }
        }
        catch (IOException e) {
            System.out.println("Bad api call");
            return false;
        }
    }

    protected void onPostExecute(String token) {
        // background work is finished,
        // we can update the UI here
        // including removing the dialog
    }
}
