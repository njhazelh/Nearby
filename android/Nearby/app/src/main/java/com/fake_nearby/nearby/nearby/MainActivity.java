package com.fake_nearby.nearby.nearby;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.preference.PreferenceManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.bluetooth.*;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Toast;

import com.fake_nearby.nearby.nearby.dummy.DummyContent;

public class MainActivity extends AppCompatActivity implements BTDeviceFragment.OnListFragmentInteractionListener {
    private BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    private ArrayAdapter<String> mArrayAdapter;
    private int REQUEST_ENABLE_BT = 1;

    // Create a BroadcastReceiver for ACTION_FOUND
    private final BroadcastReceiver mReceiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            // When discovery finds a device
            System.out.println("action " + action);
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                // Get the BluetoothDevice object from the Intent
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                int rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI, Short.MIN_VALUE);
                BTDevice btd = new BTDevice(device.getName(), device.getAddress(), rssi, false);
                // Add the name and address to an array adapter to show in the ListView
                displayDevice(btd);
                System.out.println("found something");
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (mBluetoothAdapter == null) {
            // Device does not support Bluetooth
            Toast.makeText(getApplicationContext(), "Sorry, your device does not support Bluetooth!", Toast.LENGTH_LONG).show();
        }
        else {
            Toast.makeText(getApplicationContext(), "Cool, you have Bluetooth!", Toast.LENGTH_SHORT).show();
            // start the listview fragment
            if (savedInstanceState == null) {
                getSupportFragmentManager().beginTransaction()
                        .add(R.id.btdevice_container, new BTDeviceFragment())
                        .commit();
            }

            // enable bluetooth
            if (!mBluetoothAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }

            // make discoverable for as long as the app is open
            Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
            discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 0);
            startActivityForResult(discoverableIntent, 1);

            // get the location permission
            this.getLocationPermission();

            // Register the BroadcastReceiver
            IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
            registerReceiver(mReceiver, filter); // Don't forget to unregister during onDestroy

            // Set the button to start a scan
            final Button button = (Button) findViewById(R.id.scan_btn);
            assert button != null;
            button.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    Toast.makeText(getApplicationContext(), "Scanning...", Toast.LENGTH_SHORT).show();
                    doBTScan();
                }
            });

            // Login
            this.login();
        }
    }

    public void login() {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        // send the login request
        ApiRequests.doAuthRequest(prefs.getString("username", "messedup"), prefs.getString("password", "messedup"));
        // register this device's MAC with your account
        this.addCurrentDevice();
    }

    public void addCurrentDevice() {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        String addr = mBluetoothAdapter.getAddress();
        // compatibility fix for marshmallow: always returns that address when getAddress() is called
        if (addr.equals("02:00:00:00:00:00")) {
            addr = android.provider.Settings.Secure.getString(getContentResolver(), "bluetooth_address");
        }
        // make the request to add device to account
        ApiRequests.addDevice(addr);
    }

    public void getLocationPermission() {
        // if location permission either hasn't been granted or was revoked, ask for it
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        1);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        // modify profile
        if (id == R.id.action_profile) {
            Intent intent = new Intent(this, SettingsActivity.class);
            startActivity(intent);
        }

        // create account
        if (id == R.id.action_create_account) {
            Intent intent = new Intent(this, CreateAcctActivity.class);
            startActivity(intent);
        }


        return super.onOptionsItemSelected(item);
    }

    public void doBTScan() {
        // OLD: get paired devices
        //        System.out.println(mArrayAdapter.getCount());
        // get your devices
        /*
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            // Loop through paired devices
            for (BluetoothDevice device : pairedDevices) {
                this.displayDevice(device.getName(), device.getAddress(), 0, true);
            }
        }
        */

        // get discoverable devices devices; ACTION_FOUND will automatically kick to registered receiver
        mBluetoothAdapter.startDiscovery();
    }

    // calls down to display the device in the listview
    public void displayDevice(BTDevice btd) {
        BTDeviceFragment frag = (BTDeviceFragment) getSupportFragmentManager().findFragmentById(R.id.btdevice_container);
        frag.displayDevice(btd);
    }

    /* BELOW: handlers for pausing/destroying to ensure receiver is properly registered */
    protected void onResume() {
        super.onResume();

        // Register the BroadcastReceiver
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        registerReceiver(mReceiver, filter); // Don't forget to unregister during onDestroy
        System.out.println("onresume");
        this.login();
    }

    protected void onPause() {
        super.onPause();
        if (mReceiver != null) {
            try {unregisterReceiver(mReceiver);} catch(IllegalArgumentException e) { }
        }
        System.out.println("onpause");
    }

    protected void onDestroy() {
        super.onDestroy();
        if (mReceiver != null) {
            try {unregisterReceiver(mReceiver);} catch(IllegalArgumentException e) { }
        }
        System.out.println("ondestroy");
    }
    @Override
    public void onListFragmentInteraction(DummyContent.DummyItem item) {

    }
}
