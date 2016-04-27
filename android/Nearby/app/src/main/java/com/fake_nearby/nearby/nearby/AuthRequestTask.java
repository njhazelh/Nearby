package com.fake_nearby.nearby.nearby;

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
public class AuthRequestTask extends AsyncTask<String, Boolean, Boolean>  {
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    protected void onPreExecute() {
        // perhaps show a dialog
        // with a progress bar
        // to let your users know
        // something is happening
    }

    protected Boolean doInBackground(String... aParams) {
        final OkHttpClient client = new OkHttpClient();
        final Gson gson = new Gson();
        JsonObject authJson = new JsonObject();
        authJson.addProperty("username", aParams[0]);
        authJson.addProperty("password", aParams[1]);

        RequestBody authBody = RequestBody.create(JSON, authJson.toString());
        Request request = new Request.Builder().url(ApiRequests.baseUrl + "/access").post(authBody).build();
        try {
            Response response = client.newCall(request).execute();
            if (response.code() == 200) {
                JsonParser parser = new JsonParser();
                JsonElement element = parser.parse(response.body().string());
                JsonObject jsonObject = element.getAsJsonObject();
                ApiRequests.authToken = jsonObject.get("token").getAsString();
                return true;
            }
            else {
                System.out.println("Bad http response: auth "  + response.code());
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
