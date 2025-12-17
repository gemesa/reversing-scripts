import java.io.*;
import java.util.zip.InflaterInputStream;

public class XLoaderDecryptor {

  private static final int HEADER_SIZE = 12;
  private static final int XOR_KEY_OFFSET = 11; // local_a9 = ajStack_b4[11]
  private static final int BUFFER_SIZE = 512; // 0x200

  public static void main(String[] args) throws Exception {
    String inputFile = args.length > 0 ? args[0] : "1bmurb1";
    String outputFile = args.length > 1 ? args[1] : "payload.dex";

    /*
     * Native:
     *   p_Var3 = CallObjectMethod(env, obj, getAssets)
     *   array = CallObjectMethod(env, p_Var3, list, obj2)
     *   str = GetObjectArrayElement(env, array, 0)
     *   ... build path: acStack_a8 = obj2 + "/" + str ...
     *   p_Var3 = CallObjectMethod(env, p_Var3, open, p_Var7)
     */
    byte[] data = readFile(inputFile);
    System.out.println("Input file size: " + data.length + " bytes.");

    /*
     * Native:
     *   p_Var8 = NewByteArray(env, 0xc)                    // 12-byte header
     *   CallIntMethod(env, p_Var3, read, p_Var8)           // read header
     *   GetByteArrayRegion(env, p_Var8, 0, 0xc, ajStack_b4) // copy to stack
     *   // XOR key is at ajStack_b4[11] = local_a9
     */
    byte xorKey = data[XOR_KEY_OFFSET];
    System.out.println("XOR key (offset 11): 0x" + String.format("%02x", xorKey & 0xFF) + ".");

    /*
     * Native:
     *   p_Var8 = NewByteArray(env, 0x200)                  // 512-byte buffer
     *   local_c0 = 0; local_bc = 0; local_b8 = 0;          // vector init
     *
     *   while ((iVar9 = CallIntMethod(env, p_Var3, read, p_Var8)) >= 0) {
     *       pjVar10 = GetByteArrayElements(env, p_Var8, 0)
     *       for (iVar12 = 0; iVar12 < iVar9; iVar12++) {
     *           // XOR decrypt: pjVar10[iVar12] ^ local_a9
     *           if (local_bc < local_b8) {
     *               *local_bc = pjVar10[iVar12] ^ local_a9;
     *               local_bc++;
     *           } else {
     *               vector::push_back_slow_path()
     *           }
     *       }
     *       ReleaseByteArrayElements(env, p_Var8, pjVar10, 0)
     *   }
     *   CallVoidMethod(env, p_Var3, close)
     */
    byte[] decrypted = new byte[data.length - HEADER_SIZE];
    System.arraycopy(data, HEADER_SIZE, decrypted, 0, decrypted.length);

    for (int i = 0; i < decrypted.length; i++) {
      decrypted[i] ^= xorKey;
    }
    System.out.println("Decrypted size: " + decrypted.length + " bytes.");

    /*
     * Native:
     *   array_00 = NewByteArray(env, local_bc - local_c0)
     *   SetByteArrayRegion(env, array_00, 0, local_bc - local_c0, local_c0)
     *
     *   // Create ByteArrayInputStream
     *   p_Var1 = FindClass(env, "java/io/ByteArrayInputStream")
     *   p_Var11 = GetMethodID(env, p_Var1, "<init>", "([B)V")
     *   uVar13 = NewObject(env, p_Var1, p_Var11, array_00)
     *
     *   // Create InflaterInputStream
     *   p_Var3 = createInflateStream(env, ..., uVar13, ...)
     *   // createInflateStream() does:
     *   //   FindClass("java/util/zip/InflaterInputStream")
     *   //   GetMethodID("<init>", "(Ljava/io/InputStream;)V")
     *   //   NewObject() -> new InflaterInputStream(bais)
     */
    ByteArrayInputStream bais = new ByteArrayInputStream(decrypted);
    InflaterInputStream inflater = new InflaterInputStream(bais);

    /*
     * Native:
     *   local_bc = local_c0;  // reset vector position
     *
     *   while ((iVar9 = CallIntMethod(env, p_Var3, read, p_Var8)) >= 0) {
     *       pjVar10 = GetByteArrayElements(env, p_Var8, 0)
     *       for (iVar12 = 0; iVar12 < iVar9; iVar12++) {
     *           // No XOR here - just copy decompressed bytes
     *           if (local_bc == local_b8) {
     *               vector::push_back_slow_path()
     *           } else {
     *               *local_bc = pjVar10[iVar12];
     *               local_bc++;
     *           }
     *       }
     *       ReleaseByteArrayElements(env, p_Var8, pjVar10, 0)
     *   }
     *   CallVoidMethod(env, p_Var3, close)
     */
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    byte[] buffer = new byte[BUFFER_SIZE];
    int bytesRead;
    while ((bytesRead = inflater.read(buffer)) != -1) {
      baos.write(buffer, 0, bytesRead);
    }
    inflater.close();

    /*
     * Native:
     *   p_Var8 = NewByteArray(env, local_bc - local_c0)
     *   SetByteArrayRegion(env, p_Var8, 0, local_bc - local_c0, local_c0)
     *   vector::~vector()  // cleanup
     *   return p_Var8      // return decrypted DEX bytes
     */
    byte[] decompressed = baos.toByteArray();
    System.out.println("Decompressed size: " + decompressed.length + " bytes.");

    if (decompressed[0] == 'd' && decompressed[1] == 'e' && decompressed[2] == 'x') {
      System.out.println("Found DEX file.");
    }

    writeFile(outputFile, decompressed);
    System.out.println("Saved to: " + outputFile + ".");
  }

  private static byte[] readFile(String path) throws IOException {
    FileInputStream fis = new FileInputStream(path);
    byte[] data = fis.readAllBytes();
    fis.close();
    return data;
  }

  private static void writeFile(String path, byte[] data) throws IOException {
    FileOutputStream fos = new FileOutputStream(path);
    fos.write(data);
    fos.close();
  }
}
