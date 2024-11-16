int calc_circular_distance(int a, int b, int n){
    int d1 = abs(a-b);
    int d2 = n - d1;
    if(d1 < d2){
        return d1;
    }
    return -d2;
}

int calculate_median(vector<int> arr){
    sort(arr.begin(), arr.end());
    int n = arr.size();
    if(n%2 == 0){
        return (arr[n/2] + arr[n/2-1])/2;
    }
    return arr[n/2];
}

int minOperations(int k, int n, vector<int> locks){
    vector<int> linear_distance(n,0);
    linear_distance[0] = 0;
    for(int i=0; i<n; i++){
        linear_distance[i] = calc_circular_distance(locks[i], locks[0], k);
    }
    int avg = 0;
    avg = calculate_median(linear_distance);
    int min_operations = 0;
    for(int i=0; i<n; i++){
        min_operations += abs(linear_distance[i] - avg);
    }
    return min_operations;
}


