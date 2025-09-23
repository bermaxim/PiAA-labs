import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String S = reader.readLine();
        String T = reader.readLine();

        int n = S.length();
        int m = T.length();

        // -------------------------
        // Левенштейн
        // -------------------------
        int[][] dp = new int[n + 1][m + 1];

        for (int i = 0; i <= n; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= m; j++) {
            dp[0][j] = j;
        }

        for (int i = 1; i <= n; i++) {
            char sChar = S.charAt(i - 1);
            for (int j = 1; j <= m; j++) {
                char tChar = T.charAt(j - 1);
                if (sChar == tChar) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        dp[i - 1][j - 1],
                        Math.min(
                            dp[i - 1][j],
                            dp[i][j - 1]
                        )
                    );
                }
            }
        }

        System.out.println("Расстояние Левенштейна = " + dp[n][m]);

        // -------------------------
        // Наибольшая общая подстрока (14б)
        // -------------------------
        int[][] dp2 = new int[n + 1][m + 1];
        int maxLen = 0;
        int endIndex = 0; // конец подстроки в S

        for (int i = 1; i <= n; i++) {
            char sChar = S.charAt(i - 1);
            for (int j = 1; j <= m; j++) {
                char tChar = T.charAt(j - 1);
                if (sChar == tChar) {
                    dp2[i][j] = dp2[i - 1][j - 1] + 1;
                    if (dp2[i][j] > maxLen) {
                        maxLen = dp2[i][j];
                        endIndex = i;
                    }
                } else {
                    dp2[i][j] = 0;
                }
            }
        }

        String substring = S.substring(endIndex - maxLen, endIndex);
        System.out.println("Длина наибольшей общей подстроки = " + maxLen);
        if (substring.isEmpty()) {
            System.out.println("Общая подстрока отсутствует");
        } else {
            System.out.println("Общая подстрока = " + substring);
        }
    }
}