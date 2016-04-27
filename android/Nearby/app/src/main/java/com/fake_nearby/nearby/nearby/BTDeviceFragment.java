package com.fake_nearby.nearby.nearby;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.fake_nearby.nearby.nearby.dummy.DummyContent;
import com.fake_nearby.nearby.nearby.dummy.DummyContent.DummyItem;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * A fragment representing a list of Items.
 * <p/>
 * Activities containing this fragment MUST implement the {@link OnListFragmentInteractionListener}
 * interface.
 */
public class BTDeviceFragment extends Fragment {

    // TODO: Customize parameter argument names
    private static final String ARG_COLUMN_COUNT = "column-count";
    // TODO: Customize parameters
    private int mColumnCount = 1;
    private OnListFragmentInteractionListener mListener;
    private ArrayAdapter<String> mArrayAdapter;
    private int REQUEST_ENABLE_BT = 1;


    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public BTDeviceFragment() {
    }

    // TODO: Customize parameter initialization
    @SuppressWarnings("unused")
    public static BTDeviceFragment newInstance(int columnCount) {
        BTDeviceFragment fragment = new BTDeviceFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_COLUMN_COUNT, columnCount);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (getArguments() != null) {
            mColumnCount = getArguments().getInt(ARG_COLUMN_COUNT);
        }

    }

    // @param rssi: the signal strength (paired devices will always send in 999, a value which will be ignored)
    public void displayDevice(String name, String address, int rssi, boolean paired) {
        // TODO: API CALL HERE
        // make the call and identify the user as either a registered/id'd person
        // or someone who should be identified
        if (name == null) {
            name = "";
        }
        String devTag = name + "\n" + address;
        String apiName = "";
        if (!apiName.equals("")) {
            devTag = apiName;
        }
        else if (paired) {
            devTag = "You: " + devTag;
        }
        else {
            devTag = "Unknown user " + devTag;
        }

        // add rssi for non-paired devices
        if (!paired) {
            devTag += "\n" + Integer.toString(rssi) + " dBm";
        }

        // Add the name and address to an array adapter to show in a ListView
        if (mArrayAdapter.getPosition(devTag) == -1) {
            mArrayAdapter.add(devTag);
            mArrayAdapter.notifyDataSetChanged();
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ArrayList<String> defItems = new ArrayList<String>();
        defItems.add("one");
        defItems.add("two");
        defItems.add("three");
        mArrayAdapter = new ArrayAdapter<String>(getActivity(), R.layout.fragment_btdevice, R.id.content1, defItems);
        View view = inflater.inflate(R.layout.fragment_btdevice_list, container, false);
        ListView listView = (ListView) view.findViewById(R.id.fragment_btdevice_list);
        listView.setAdapter(mArrayAdapter);


        // TODO
        /*listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(getActivity(), IdentifyDeviceActivity.class);
                intent.putExtra(Intent.EXTRA_TEXT, mArrayAdapter.getItem(i));
                startActivity(intent);
            }
        });*/
        // OLD
        // Set the adapter
        /*if (view instanceof RecyclerView) {
            Context context = view.getContext();
            RecyclerView recyclerView = (RecyclerView) view;
            if (mColumnCount <= 1) {
                recyclerView.setLayoutManager(new LinearLayoutManager(context));
            } else {
                recyclerView.setLayoutManager(new GridLayoutManager(context, mColumnCount));
            }
            recyclerView.setAdapter(new MyBTDeviceRecyclerViewAdapter(DummyContent.ITEMS, mListener));
        }*/

        return view;
    }

    /*
    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof OnListFragmentInteractionListener) {
            mListener = (OnListFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnListFragmentInteractionListener");
        }
    }
    */
    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnListFragmentInteractionListener {
        // TODO: Update argument type and name
        void onListFragmentInteraction(DummyItem item);
    }
}
