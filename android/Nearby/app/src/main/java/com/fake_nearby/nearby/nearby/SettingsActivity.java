package com.fake_nearby.nearby.nearby;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceActivity;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;

public class SettingsActivity extends PreferenceActivity implements SharedPreferences.OnSharedPreferenceChangeListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Display the fragment as the main content.
        getFragmentManager().beginTransaction()
                .replace(android.R.id.content, new SettingsFragment())
                .commit();

        // register listener for shared preferences
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        prefs.registerOnSharedPreferenceChangeListener(this);
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences,
                                          String key) {
        System.out.println("shared pref changed!");
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        // if anything is changed for the display name, username, or password, send a put request to the server
        try {
            if (key.equals("firstlast") || key.equals("username") || key.equals("password")) {
                ApiRequests.accountService(prefs.getString("username", "messedup"), prefs.getString("password", "messedup"), prefs.getString("firstlast", "messed up"), "modify");
            }
        }
        catch (Exception e) {
            System.out.println("Something went wrong in API");
        }
    }

    public static class SettingsFragment extends PreferenceFragment {
        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            // Load the preferences from an XML resource
            addPreferencesFromResource(R.xml.prefs);
        }
    }
}
