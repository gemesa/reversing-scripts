import java.util.Base64;

public class ChromeUpdaterCrypt {
    
    private static byte[] xorCrypt(byte[] data, String key) {
        int length = data.length;
        int keyLength = key.length();
        int keyIndex = 0;
        
        for (int i = 0; i < length; i++) {
            if (keyIndex >= keyLength) {
                keyIndex = 0;
            }
            data[i] = (byte) (data[i] ^ key.charAt(keyIndex));
            keyIndex++;
        }
        return data;
    }
    
    public static String encrypt(String plaintext, String key) {
        byte[] data = plaintext.getBytes();
        byte[] encrypted = xorCrypt(data, key);
        return Base64.getEncoder().encodeToString(encrypted);
    }
    
    public static String decrypt(String encodedStr, String key) {
        byte[] decoded = Base64.getDecoder().decode(encodedStr);
        byte[] decrypted = xorCrypt(decoded, key);
        return new String(decrypted);
    }
    
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java ChromeUpdaterCrypt <d|e> <string>");
            System.out.println("  d - Decode (decrypt) a Base64+XOR encoded string");
            System.out.println("  e - Encode (encrypt) a plaintext string");
            System.out.println();
            System.out.println("Examples:");
            System.out.println("  java ChromeUpdaterCrypt d \"Gh8=\"");
            System.out.println("  java ChromeUpdaterCrypt e \"OK\"");
            System.exit(1);
        }
        
        String command = args[0];
        String input = args[1];
        String key = "UTF-8";
        
        try {
            switch (command.toLowerCase()) {
                case "d":
                    String decoded = decrypt(input, key);
                    System.out.println(decoded);
                    break;
                    
                case "e":
                    String encoded = encrypt(input, key);
                    System.out.println(encoded);
                    break;
                    
                default:
                    System.err.println("Error: Unknown command '" + command + "'");
                    System.err.println("Use 'd' for decode or 'e' for encode");
                    System.exit(1);
            }
        } catch (IllegalArgumentException e) {
            System.err.println("Error: Invalid Base64 input for decoding");
            System.exit(1);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
