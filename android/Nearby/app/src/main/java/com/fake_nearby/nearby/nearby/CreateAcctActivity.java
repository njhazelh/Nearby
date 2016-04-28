package com.fake_nearby.nearby.nearby;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceActivity;
import android.preference.PreferenceFragment;
import android.preference.PreferenceManager;

public class CreateAcctActivity extends PreferenceActivity implements SharedPreferences.OnSharedPreferenceChangeListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Display the fragment as the main content.
        getFragmentManager().beginTransaction()
                .replace(android.R.id.content, new SettingsFragment())
                .commit();
    }

    @Override
    public void onSharedPreferenceChanged(SharedPreferences sharedPreferences,
                                          String key) {
        // this is handled in settingsactivity and the settingsfragment here
    }

    public static class SettingsFragment extends PreferenceFragment {
        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            // Load the preferences from an XML resource
            addPreferencesFromResource(R.xml.create_prefs);

            Preference button = findPreference("closeandsave");
            // if the "save" button is hit, set a post request to the server to create a new account
            // because it's shared prefs, this will auto-update the logged in account in "modify profile"
            button.setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
                @Override
                public boolean onPreferenceClick(Preference preference) {
                    final SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getActivity());
                    ApiRequests.accountService(prefs.getString("username", "messedup"), prefs.getString("password", "messedup"), prefs.getString("firstlast", "messed up"), "create");
                    return true;
                }
            });
        }
    }
}
