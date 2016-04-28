package com.fake_nearby.nearby.nearby;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.fake_nearby.nearby.nearby.dummy.DummyContent.DummyItem;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

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
    private ArrayList<String> devicesSeen = new ArrayList<String>();
    static final String ALONE = "Nobody nearby right now :(";


    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public BTDeviceFragment() {
    }

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

    // display a device in the listview by querying server for saved name
    public void displayDevice(BTDevice btd) {
        // do duplicate checking with mac addresses
        if (!devicesSeen.contains(btd.mac)) {
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mmZ");
            String now = df.format(new Date());
            // report observations and get names of anyone observed
            ApiRequests.reportObservation(now, btd.mac, btd.rssi);
            new GetNamesTask().execute(btd);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ArrayList<String> defItems = new ArrayList<String>();
        defItems.add(ALONE);
        mArrayAdapter = new ArrayAdapter<String>(getActivity(), R.layout.fragment_btdevice, R.id.content1, defItems);
        View view = inflater.inflate(R.layout.fragment_btdevice_list, container, false);
        ListView listView = (ListView) view.findViewById(R.id.fragment_btdevice_list);
        listView.setAdapter(mArrayAdapter);


        // TODO: would need to set onclicklistener to see more profile information for users
        /*listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Intent intent = new Intent(getActivity(), IdentifyDeviceActivity.class);
                intent.putExtra(Intent.EXTRA_TEXT, mArrayAdapter.getItem(i));
                startActivity(intent);
            }
        });*/
        return view;
    }

    /* UNUSED
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

    /**
     * Created by Lyn on 4/26/2016.
     */
    private class GetNamesTask extends AsyncTask<BTDevice, Boolean, Boolean> {
        public final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

        protected void onPreExecute() {
            // perhaps show a dialog
            // with a progress bar
            // to let your users know
            // something is happening
        }

        protected Boolean doInBackground(BTDevice... aParams) {
            final OkHttpClient client = new OkHttpClient();
            // get names of nearby users
            Request request = new Request.Builder().url(ApiRequests.baseUrl + "/users/nearby").addHeader("Authentication", ApiRequests.authToken).build();
            try {
                Response response = client.newCall(request).execute();
                if (response.code() == 200) { // if it worked, parse the array and display all
                    JsonParser parser = new JsonParser();
                    JsonElement element = parser.parse(response.body().string());
                    JsonObject jsonObject = element.getAsJsonObject();
                    final JsonArray all_users = jsonObject.get("users").getAsJsonArray();
                    // ui updates cannot be done on a separate thread, so return to the main one
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            for (JsonElement user : all_users) {
                                // display every user's full name if they haven't been displayed already
                                String name = user.getAsJsonObject().get("first_name").getAsString() + " " + user.getAsJsonObject().get("last_name").getAsString();

                                if (mArrayAdapter.getPosition(name) == -1) {
                                    mArrayAdapter.add(user.getAsJsonObject().get("first_name").getAsString() + " " + user.getAsJsonObject().get("last_name").getAsString());
                                    mArrayAdapter.notifyDataSetChanged();
                                    if (devicesSeen.size() == 0) {
                                        // remove the "haven't seen anybody" message
                                        mArrayAdapter.remove(ALONE);
                                    }
                                }
                            }
                        }
                    });


                    return true;
                }
                else {
                    System.out.println("Bad http response: get names "  + response.code());
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

}
