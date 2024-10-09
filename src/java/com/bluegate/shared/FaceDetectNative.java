package com.bluegate.shared;

public class FaceDetectNative {
    static {
        java.lang.System.loadLibrary("native-lib");
    }

    public static native int[] getFacialLandmarks(byte[] bArr, long j, long j2, int i);
}
