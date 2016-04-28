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
        if (givenName == null) {
            this.name = ""; // TODO: "Unknown user"?
        }
        else {
            this.name = givenName;
        }
        this.mac = mac;
        this.rssi = rssi;
        this.paired = paired;
    }

    @Override
    // old; used when printing everybody in an area instead of just known users
    public String toString() {
        return this.name + "\n" + this.mac + "\n" + this.rssi + " dBm";
    }

}
