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
public class AcctTask extends AsyncTask<String, Boolean, Boolean>  {
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
        // if an account is being created, all of these are necessary
        // if it's just being modified, we don't _need_ all of these, but including them doesn't hurt
        authJson.addProperty("username", aParams[0]);
        authJson.addProperty("password", aParams[1]);
        authJson.addProperty("first_name", aParams[2]);
        authJson.addProperty("last_name", aParams[3]);

        RequestBody authBody = RequestBody.create(JSON, authJson.toString());
        Request request;

        // switch based on modification or creation of an account; adds auth token when appropriate
        // if an account is created, it'll be logged in upon return to main screen
        switch(aParams[4]) {
            case "create":
                request = new Request.Builder().url(ApiRequests.baseUrl + "/users").post(authBody).build();
                break;
            default: //case "modify":
                request = new Request.Builder().url(ApiRequests.baseUrl + "/users").put(authBody).addHeader("Authentication", ApiRequests.authToken).build();
                break;
        }

        try {
            Response response = client.newCall(request).execute();
            JsonParser parser = new JsonParser();
            JsonElement element = parser.parse(response.body().string());
            JsonObject jsonObject = element.getAsJsonObject();
            if (response.code() == 200) {
                //System.out.println(jsonObject.get("message").getAsString());
                return true;
            }
            else if (response.code() == 400) {
                System.out.println(jsonObject.get("error").getAsString());
                return false;
            }
            else {
                System.out.println("Bad http response: acct task "  + response.code());
                System.out.println(authBody.toString());
                System.out.println(request.toString());
                return false;
            }
        }
        catch (Exception e) {
            System.out.println("Bad api call");
            System.out.println(request.toString());
            return false;
        }
    }

    protected void onPostExecute(String token) {
        // background work is finished,
        // we can update the UI here
        // including removing the dialog
    }
}
