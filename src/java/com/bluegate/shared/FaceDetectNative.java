package com.bluegate.shared;

public class FaceDetectNative {

    static {
        System.loadLibrary("native-lib");
    }

    static String intToHexString(int[] iArr) {
        StringBuilder sb2 = new StringBuilder();
        int length = iArr.length;

        for (int i10 = 0; i10 < length; i10++) {
            sb2.append(String.format("%02X", new Object[] { iArr[i10] }));
        }

        return sb2.toString();
    }

    static byte[] hexStringToByteArray(String str) {
        int length = str.length();

        byte[] bArr = new byte[(length / 2)];
        for (int i10 = 0; i10 < length; i10 += 2) {
            bArr[i10 / 2] = (byte) (Character.digit(str.charAt(i10 + 1), 16)
                    + (Character.digit(str.charAt(i10), 16) << 4));
        }

        return bArr;
    }


    public static String getToken(String sessionToken, String userId) {
        long ts = 1L + System.currentTimeMillis() / 1000;
        byte[] sessionTokenBytes = hexStringToByteArray(sessionToken);
        long userIdLong = Long.parseLong(userId);
        return intToHexString(getFacialLandmarks(sessionTokenBytes, ts, userIdLong, 1));
    }
    
    public static native int[] getFacialLandmarks(byte[] sessionTokenBytes, long ts, long userId, int type);


}