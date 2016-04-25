package com.fake_nearby.nearby.nearby;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
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

import java.util.Set;

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
                // Add the name and address to an array adapter to show in a ListView
                displayDevice(device.getName(), device.getAddress(), rssi, false);
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
            startActivityForResult(new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE), 1);

            // Register the BroadcastReceiver
            IntentFilter fltr = new IntentFilter();
            fltr = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
            fltr.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
            fltr.addAction(BluetoothDevice.ACTION_FOUND);
            //IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
            registerReceiver(mReceiver, fltr); // Don't forget to unregister during onDestroy

            // Set the button to start a scan
            final Button button = (Button) findViewById(R.id.scan_btn);
            assert button != null;
            button.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    Toast.makeText(getApplicationContext(), "Scanning...", Toast.LENGTH_SHORT).show();
                    doBTScan();
                }
            });

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

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_profile) {
            Intent intent = new Intent(this, SettingsActivity.class);
            startActivity(intent);
        }

        return super.onOptionsItemSelected(item);
    }

    public void doBTScan() {
//        System.out.println(mArrayAdapter.getCount());
        // get your devices
        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            // Loop through paired devices
            for (BluetoothDevice device : pairedDevices) {
                this.displayDevice(device.getName(), device.getAddress(), 0, true);
            }
        }
        // get other available devices
        mBluetoothAdapter.startDiscovery();
    }

    // @param rssi: the signal strength (paired devices will always send in 999, a value which will be ignored)
    public void displayDevice(String name, String address, int rssi, boolean paired) {
        BTDeviceFragment frag = (BTDeviceFragment) getSupportFragmentManager().findFragmentById(R.id.btdevice_container);
        frag.displayDevice(name, address, rssi, paired);
    }

    protected void onResume() {
        super.onResume();

        // Register the BroadcastReceiver
        IntentFilter fltr = new IntentFilter();
        fltr = new IntentFilter(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        fltr.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        fltr.addAction(BluetoothDevice.ACTION_FOUND);
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        registerReceiver(mReceiver, fltr); // Don't forget to unregister during onDestroy
        System.out.println("onresume");
    }

    protected void onPause() {
        super.onPause();
        if (mReceiver != null) {
            unregisterReceiver(mReceiver);
        }
        System.out.println("onpause");
    }

    protected void onDestroy() {
        super.onDestroy();
        if (mReceiver != null) {
            unregisterReceiver(mReceiver);
        }
        System.out.println("ondestroy");
    }
    @Override
    public void onListFragmentInteraction(DummyContent.DummyItem item) {

    }
}
