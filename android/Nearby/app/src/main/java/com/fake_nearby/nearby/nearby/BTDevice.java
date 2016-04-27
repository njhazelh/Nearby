package com.fake_nearby.nearby.nearby;

/**
 * Created by Lyn on 4/27/2016.
 */
public class BTDevice {
    public String name;
    public String mac;
    public int rssi;
    public boolean paired;

    public BTDevice(String givenName, String mac, int rssi, boolean paired) {
        //  TODO: api call to get name
        if (givenName == null) {
            this.name = "";
        }
        else {
            this.name = givenName;
        }
        this.mac = mac;
        this.rssi = rssi;
        this.paired = paired;
    }

    @Override
    public String toString() {
        return this.name + "\n" + this.mac + "\n" + this.rssi + " dBm";
    }

}
