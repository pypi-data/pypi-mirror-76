from pathlib import Path
from unittest import TestCase

from sekg.so.code_content_classification import CodeContentClassification
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCodeContentClassification(TestCase):
    def test_so_text_label(self):
        cc = CodeContentClassification()
        t = """
                public class Test {

                  public static int LOOP_ITERATION= 100000;

                  public static void stringTest(){
                    long startTime = System.currentTimeMillis();
                    String string = "This";
                    for(int i=0;i&lt;LOOP_ITERATION;i++){
                        string = string+"Yasir";
                    }

                    long endTime = System.currentTimeMillis();
                    System.out.println(endTime - startTime);    
                  }

                  public static void stringBufferTest(){
                    long startTime = System.currentTimeMillis();
                    StringBuffer stringBuffer = new StringBuffer("This");
                    for(int i=0;i&lt;LOOP_ITERATION;i++){
                        stringBuffer.append("Yasir");
                    }

                    long endTime = System.currentTimeMillis();
                    System.out.println(endTime - startTime);
                  }

                  public static void main(String []args){
                    stringTest()
                    stringBufferTest(); 
                  }
                 }
                """
        self.assertEqual(True, cc.check_is_code(t))
        t = """string += newString;
        """
        self.assertEqual(True, cc.check_is_code(t))
        t = """StringBuffer is not. It is thread safe. """
        self.assertEqual(False, cc.check_is_code(t))

    def test_case_for_code(self):
        code_list = [
            """ArrayList aList = new ArrayList();

//Add elements to ArrayList object
aList.add("1");
aList.add("2");
aList.add("3");
aList.add("4");
aList.add("5");

while (aList.listIterator().hasPrevious())
  Log.d("reverse", "" + aList.listIterator().previous());""",
            """
            Collections.reverse(aList);
            """,

            """Field f = obj.getClass().getDeclaredField("stuffIWant"); //NoSuchFieldException
f.setAccessible(true);
Hashtable iWantThis = (Hashtable) f.get(obj); //IllegalAccessException
""", """org.hamcrest.Matchers.*
org.hamcrest.CoreMatchers.*
org.junit.*
org.junit.Assert.*
org.junit.Assume.*
org.junit.matchers.JUnitMatchers.*""", """obj.getClass().getDeclaredField("misspelled"); //will throw NoSuchFieldException
""", """File f = new File(filePathString);
if(f.exists() && !f.isDirectory()) { 
    // do something
}
""", """public class SomeView {
    private UserLister userLister;

    public void render() {
        List<User> users = userLister.getUsers();
        view.render(users);
    }
}""", """public class Test {
    int value;


    public int getValue() {
        return value;
    }

    public void reset() {
        value = 0;
    }

    // Calculates without exception
    public void method1(int i) {
        value = ((value + i) / i) << 1;
        // Will never be true
        if ((i & 0xFFFFFFF) == 1000000000) {
            System.out.println("You'll never see this!");
        }
    }

    // Could in theory throw one, but never will
    public void method2(int i) throws Exception {
        value = ((value + i) / i) << 1;
        // Will never be true
        if ((i & 0xFFFFFFF) == 1000000000) {
            throw new Exception();
        }
    }

    // This one will regularly throw one
    public void method3(int i) throws Exception {
        value = ((value + i) / i) << 1;
        // i & 1 is equally fast to calculate as i & 0xFFFFFFF; it is both
        // an AND operation between two integers. The size of the number plays
        // no role. AND on 32 BIT always ANDs all 32 bits
        if ((i & 0x1) == 1) {
            throw new Exception();
        }
    }

    public static void main(String[] args) {
        int i;
        long l;
        Test t = new Test();

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            t.method1(i);
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method1 took " + l + " ms, result was " + t.getValue()
        );

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            try {
                t.method2(i);
            } catch (Exception e) {
                System.out.println("You'll never see this!");
            }
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method2 took " + l + " ms, result was " + t.getValue()
        );

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            try {
                t.method3(i);
            } catch (Exception e) {
                // Do nothing here, as we will get here
            }
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method3 took " + l + " ms, result was " + t.getValue()
        );
    }
}""", """if((x & 4294967295LL) == 0)
    x >>= 32;
if((x & 65535) == 0)
    x >>= 16;
if((x & 255) == 0)
    x >>= 8;
if((x & 15) == 0)
    x >>= 4;
if((x & 3) == 0)
    x >>= 2;""", """typedef signed long long int int64;

int start[1024] =
{1,3,1769,5,1937,1741,7,1451,479,157,9,91,945,659,1817,11,
1983,707,1321,1211,1071,13,1479,405,415,1501,1609,741,15,339,1703,203,
129,1411,873,1669,17,1715,1145,1835,351,1251,887,1573,975,19,1127,395,
1855,1981,425,453,1105,653,327,21,287,93,713,1691,1935,301,551,587,
257,1277,23,763,1903,1075,1799,1877,223,1437,1783,859,1201,621,25,779,
1727,573,471,1979,815,1293,825,363,159,1315,183,27,241,941,601,971,
385,131,919,901,273,435,647,1493,95,29,1417,805,719,1261,1177,1163,
1599,835,1367,315,1361,1933,1977,747,31,1373,1079,1637,1679,1581,1753,1355,
513,1539,1815,1531,1647,205,505,1109,33,1379,521,1627,1457,1901,1767,1547,
1471,1853,1833,1349,559,1523,967,1131,97,35,1975,795,497,1875,1191,1739,
641,1149,1385,133,529,845,1657,725,161,1309,375,37,463,1555,615,1931,
1343,445,937,1083,1617,883,185,1515,225,1443,1225,869,1423,1235,39,1973,
769,259,489,1797,1391,1485,1287,341,289,99,1271,1701,1713,915,537,1781,
1215,963,41,581,303,243,1337,1899,353,1245,329,1563,753,595,1113,1589,
897,1667,407,635,785,1971,135,43,417,1507,1929,731,207,275,1689,1397,
1087,1725,855,1851,1873,397,1607,1813,481,163,567,101,1167,45,1831,1205,
1025,1021,1303,1029,1135,1331,1017,427,545,1181,1033,933,1969,365,1255,1013,
959,317,1751,187,47,1037,455,1429,609,1571,1463,1765,1009,685,679,821,
1153,387,1897,1403,1041,691,1927,811,673,227,137,1499,49,1005,103,629,
831,1091,1449,1477,1967,1677,697,1045,737,1117,1737,667,911,1325,473,437,
1281,1795,1001,261,879,51,775,1195,801,1635,759,165,1871,1645,1049,245,
703,1597,553,955,209,1779,1849,661,865,291,841,997,1265,1965,1625,53,
1409,893,105,1925,1297,589,377,1579,929,1053,1655,1829,305,1811,1895,139,
575,189,343,709,1711,1139,1095,277,993,1699,55,1435,655,1491,1319,331,
1537,515,791,507,623,1229,1529,1963,1057,355,1545,603,1615,1171,743,523,
447,1219,1239,1723,465,499,57,107,1121,989,951,229,1521,851,167,715,
1665,1923,1687,1157,1553,1869,1415,1749,1185,1763,649,1061,561,531,409,907,
319,1469,1961,59,1455,141,1209,491,1249,419,1847,1893,399,211,985,1099,
1793,765,1513,1275,367,1587,263,1365,1313,925,247,1371,1359,109,1561,1291,
191,61,1065,1605,721,781,1735,875,1377,1827,1353,539,1777,429,1959,1483,
1921,643,617,389,1809,947,889,981,1441,483,1143,293,817,749,1383,1675,
63,1347,169,827,1199,1421,583,1259,1505,861,457,1125,143,1069,807,1867,
2047,2045,279,2043,111,307,2041,597,1569,1891,2039,1957,1103,1389,231,2037,
65,1341,727,837,977,2035,569,1643,1633,547,439,1307,2033,1709,345,1845,
1919,637,1175,379,2031,333,903,213,1697,797,1161,475,1073,2029,921,1653,
193,67,1623,1595,943,1395,1721,2027,1761,1955,1335,357,113,1747,1497,1461,
1791,771,2025,1285,145,973,249,171,1825,611,265,1189,847,1427,2023,1269,
321,1475,1577,69,1233,755,1223,1685,1889,733,1865,2021,1807,1107,1447,1077,
1663,1917,1129,1147,1775,1613,1401,555,1953,2019,631,1243,1329,787,871,885,
449,1213,681,1733,687,115,71,1301,2017,675,969,411,369,467,295,693,
1535,509,233,517,401,1843,1543,939,2015,669,1527,421,591,147,281,501,
577,195,215,699,1489,525,1081,917,1951,2013,73,1253,1551,173,857,309,
1407,899,663,1915,1519,1203,391,1323,1887,739,1673,2011,1585,493,1433,117,
705,1603,1111,965,431,1165,1863,533,1823,605,823,1179,625,813,2009,75,
1279,1789,1559,251,657,563,761,1707,1759,1949,777,347,335,1133,1511,267,
833,1085,2007,1467,1745,1805,711,149,1695,803,1719,485,1295,1453,935,459,
1151,381,1641,1413,1263,77,1913,2005,1631,541,119,1317,1841,1773,359,651,
961,323,1193,197,175,1651,441,235,1567,1885,1481,1947,881,2003,217,843,
1023,1027,745,1019,913,717,1031,1621,1503,867,1015,1115,79,1683,793,1035,
1089,1731,297,1861,2001,1011,1593,619,1439,477,585,283,1039,1363,1369,1227,
895,1661,151,645,1007,1357,121,1237,1375,1821,1911,549,1999,1043,1945,1419,
1217,957,599,571,81,371,1351,1003,1311,931,311,1381,1137,723,1575,1611,
767,253,1047,1787,1169,1997,1273,853,1247,413,1289,1883,177,403,999,1803,
1345,451,1495,1093,1839,269,199,1387,1183,1757,1207,1051,783,83,423,1995,
639,1155,1943,123,751,1459,1671,469,1119,995,393,219,1743,237,153,1909,
1473,1859,1705,1339,337,909,953,1771,1055,349,1993,613,1393,557,729,1717,
511,1533,1257,1541,1425,819,519,85,991,1693,503,1445,433,877,1305,1525,
1601,829,809,325,1583,1549,1991,1941,927,1059,1097,1819,527,1197,1881,1333,
383,125,361,891,495,179,633,299,863,285,1399,987,1487,1517,1639,1141,
1729,579,87,1989,593,1907,839,1557,799,1629,201,155,1649,1837,1063,949,
255,1283,535,773,1681,461,1785,683,735,1123,1801,677,689,1939,487,757,
1857,1987,983,443,1327,1267,313,1173,671,221,695,1509,271,1619,89,565,
127,1405,1431,1659,239,1101,1159,1067,607,1565,905,1755,1231,1299,665,373,
1985,701,1879,1221,849,627,1465,789,543,1187,1591,923,1905,979,1241,181};

bool bad255[512] =
{0,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,
 1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,
 0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,
 1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,
 1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,
 1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,
 1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,
 1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
 0,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,
 1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,
 0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,
 1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,
 1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,
 1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,
 1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,
 1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
 0,0};

inline bool square( int64 x ) {
    // Quickfail
    if( x < 0 || (x&2) || ((x & 7) == 5) || ((x & 11) == 8) )
        return false;
    if( x == 0 )
        return true;

    // Check mod 255 = 3 * 5 * 17, for fun
    int64 y = x;
    y = (y & 4294967295LL) + (y >> 32);
    y = (y & 65535) + (y >> 16);
    y = (y & 255) + ((y >> 8) & 255) + (y >> 16);
    if( bad255[y] )
        return false;

    // Divide out powers of 4 using binary search
    if((x & 4294967295LL) == 0)
        x >>= 32;
    if((x & 65535) == 0)
        x >>= 16;
    if((x & 255) == 0)
        x >>= 8;
    if((x & 15) == 0)
        x >>= 4;
    if((x & 3) == 0)
        x >>= 2;

    if((x & 7) != 1)
        return false;

    // Compute sqrt using something like Hensel's lemma
    int64 r, t, z;
    r = start[(x >> 3) & 1023];
    do {
        z = x - r * r;
        if( z == 0 )
            return true;
        if( z < 0 )
            return false;
        t = z & (-z);
        r += (z & t) >> 1;
        if( r > (t  >> 1) )
            r = t - r;
    } while( t <= (1LL << 33) );

    return false;
}"""
        ]
        cc = CodeContentClassification()
        for code_text in code_list:
            check = cc.check_is_code(code_text)
            if not check:
                print(check)
            self.assertEqual(True, cc.check_is_code(code_text))
            self.assertEqual(False, cc.check_is_trace(code_text))

    def test_case_for_trace(self):
        t_list = [
            """06-03 15:05:29.614: ERROR/AndroidRuntime(7737): java.lang.UnsupportedOperationException
06-03 15:05:29.614: ERROR/AndroidRuntime(7737):     at java.util.AbstractList.remove(AbstractList.java:645)
""", """java.sql.SQLException: No suitable driver found for jdbc:mysql://database/table
    at java.sql.DriverManager.getConnection(DriverManager.java:689)
    at java.sql.DriverManager.getConnection(DriverManager.java:247)
""", """W/System.err(  901): javax.net.ssl.SSLException: Not trusted server certificate 
W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.OpenSSLSocketImpl.startHandshake(OpenSSLSocketImpl.java:360) 
W/System.err(  901):    at org.apache.http.conn.ssl.AbstractVerifier.verify(AbstractVerifier.java:92) 
W/System.err(  901):    at org.apache.http.conn.ssl.SSLSocketFactory.connectSocket(SSLSocketFactory.java:321) 
W/System.err(  901):    at org.apache.http.impl.conn.DefaultClientConnectionOperator.openConnection(DefaultClientConnectionOperator.java:129) 
W/System.err(  901):    at org.apache.http.impl.conn.AbstractPoolEntry.open(AbstractPoolEntry.java:164) 
W/System.err(  901):    at org.apache.http.impl.conn.AbstractPooledConnAdapter.open(AbstractPooledConnAdapter.java:119) 
W/System.err(  901):    at org.apache.http.impl.client.DefaultRequestDirector.execute(DefaultRequestDirector.java:348) 
W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:555) 
W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:487) 
W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:465) 
W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity.connect(MainActivity.java:129) 
W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity.access$0(MainActivity.java:77) 
W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity$2.run(MainActivity.java:49) 
W/System.err(  901): Caused by: java.security.cert.CertificateException: java.security.InvalidAlgorithmParameterException: the trust anchors set is empty 
W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.TrustManagerImpl.checkServerTrusted(TrustManagerImpl.java:157) 
W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.OpenSSLSocketImpl.startHandshake(OpenSSLSocketImpl.java:355) 
W/System.err(  901):    ... 12 more 
W/System.err(  901): Caused by: java.security.InvalidAlgorithmParame
""", """However, I get a NoSuchElementException (since there is no invocation of hasNext) Exception in thread "main" java.util.NoSuchElementException
at java.util.AbstractList$Itr.next(AbstractList.java:364)
at Main$$Lambda$1/1175962212.get(Unknown Source)
at java.util.stream.StreamSpliterators$InfiniteSupplyingSpliterator$OfRef.tryAdvance(StreamSpliterators.java:1351)
at java.util.Spliterator.forEachRemaining(Spliterator.java:326)
at java.util.stream.ReferencePipeline$Head.forEach(ReferencePipeline.java:580)
at Main.main(Main.java:20)""",
            """[INFO] --- maven-surefire-plugin:2.18.1:test (default-test) @ recorder ---
[INFO] Surefire report directory: /lhome/code/recorder/target/surefire-reports
[INFO] Using configured provider org.apache.maven.surefire.junitcore.JUnitCoreProvider
[INFO] parallel='none', perCoreThreadCount=true, threadCount=0, useUnlimitedThreads=false, threadCountSuites=0,     threadCountClasses=0, threadCountMethods=0, parallelOptimized=true
""", """Error: Could not find or load main class org.apache.maven.surefire.booter.ForkedBooter

Results :

Tests run: 0, Failures: 0, Errors: 0, Skipped: 0""", """[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test (default-test) on project recorder: Execution default-test of goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test failed: The forked VM terminated without properly saying goodbye. VM crash or System.exit called?
""", """213


40
Recently coming to a new project, I'm trying to compile our source code. Everything worked fine yesterday, but today is another story.

Every time I'm running mvn clean install on a module, once reaching the tests, it crashes into an error:

[INFO] --- maven-surefire-plugin:2.18.1:test (default-test) @ recorder ---
[INFO] Surefire report directory: /lhome/code/recorder/target/surefire-reports
[INFO] Using configured provider org.apache.maven.surefire.junitcore.JUnitCoreProvider
[INFO] parallel='none', perCoreThreadCount=true, threadCount=0, useUnlimitedThreads=false, threadCountSuites=0,     threadCountClasses=0, threadCountMethods=0, parallelOptimized=true
""", """Error: Could not find or load main class org.apache.maven.surefire.booter.ForkedBooter

Results :

Tests run: 0, Failures: 0, Errors: 0, Skipped: 0
and later on:

[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test (default-test) on project recorder: Execution default-test of goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test failed: The forked VM terminated without properly saying goodbye. VM crash or System.exit called?
I'm running on Debian 9 (Stretch) 64-bits with OpenJDK 1.8.0_181, Maven 3.5.4, working behind my company proxy which I configured in my ~/.m2/settings.xml.

A strange thing it that the latest Surefire version is 2.22.1 if I remember correctly. I tried to specify the plugin version, but it does not get updated, otherwise there's no plugin version specification in any POM (parent, grand-parent or this one).

I managed to force Maven to change the Surefire version to the latest, but now it's even worse:"""
        ]
        cc = CodeContentClassification()
        for t in t_list:
            self.assertEqual(True, cc.check_is_trace(t))

    def test_xml_or_json(self):
        t_list = ["""<project>
  [...]
  <build>
    [...]
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration>
          <source>1.8</source>
          <target>1.8</target>
        </configuration>
      </plugin>
    </plugins>
    [...]
  </build>
  [...]
</project>""", """<bean id="userLister" class="UserListerDB" />

<bean class="SomeView">
    <property name="userLister" ref="userLister" />
</bean>""", """<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <configuration>
                <source>1.8</source>
                <target>1.8</target>
            </configuration>
        </plugin>
    </plugins>
</build>""", """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>SO question 4112686</title>
        <script src="http://code.jquery.com/jquery-latest.min.js"></script>
        <script>
            $(document).on("click", "#somebutton", function() { // When HTML DOM "click" event is invoked on element with ID "somebutton", execute the following function...
                $.get("someservlet", function(responseText) {   // Execute Ajax GET request on URL of "someservlet" and execute the following function with Ajax response text...
                    $("#somediv").text(responseText);           // Locate HTML DOM element with ID "somediv" and set its text content with the response text.
                });
            });
        </script>
    </head>
    <body>
        <button id="somebutton">press here</button>
        <div id="somediv"></div>
    </body>
</html>""", """
{
  "applesDO" : [
    {
      "apple" : "Green Apple"
    },
    {
      "apple" : "Red Apple"
    }
  ]
}"""
                  ]
        cc = CodeContentClassification()
        for t in t_list:
            self.assertEqual(True, cc.check_xml(t) or cc.check_json(t))

    def test_nums(self):
        t_list = ["""[7.0, 9.0, 5.0, 1.0, 3.0 ]""", """  PID      Vss      Rss      Pss      Uss  cmdline
  890   84456K   48668K   25850K   21284K  system_server
 1231   50748K   39088K   17587K   13792K  com.android.launcher2
  947   34488K   28528K   10834K    9308K  com.android.wallpaper
  987   26964K   26956K    8751K    7308K  com.google.process.gapps
  954   24300K   24296K    6249K    4824K  com.android.phone
  948   23020K   23016K    5864K    4748K  com.android.inputmethod.latin
  888   25728K   25724K    5774K    3668K  zygote
  977   24100K   24096K    5667K    4340K  android.process.acore
...
   59     336K     332K      99K      92K  /system/bin/installd
   60     396K     392K      93K      84K  /system/bin/keystore
   51     280K     276K      74K      68K  /system/bin/servicemanager
   54     256K     252K      69K      64K  /system/bin/debuggerd""",
                  """
                              SI     BINARY

                   0:        0 B        0 B
                  27:       27 B       27 B
                 999:      999 B      999 B
                1000:     1.0 kB     1000 B
                1023:     1.0 kB     1023 B
                1024:     1.0 kB    1.0 KiB
                1728:     1.7 kB    1.7 KiB
              110592:   110.6 kB  108.0 KiB
             7077888:     7.1 MB    6.8 MiB
           452984832:   453.0 MB  432.0 MiB
         28991029248:    29.0 GB   27.0 GiB
       1855425871872:     1.9 TB    1.7 TiB
 9223372036854775807:     9.2 EB    8.0 EiB   (Long.MAX_VALUE)
""", """Test1 Times (ms)           Test2 Times (ms)
----------------           ----------------
           187                          0
           203                          0
           203                          0
           188                          0
           188                          0
           187                          0
           203                          0
           188                          0
           188                          0
           203                          0""", """999199.1231231235 == 999199.1231231236 // true
1.03 - 0.41 // 0.6200000000000001"""
                  ]
        cc = CodeContentClassification()
        for t in t_list:
            self.assertEqual(True, cc.check_nums(t))

    def test_text(self):
        t_list = [
            """Window > Preferences > Java > Editor > Content Assist > Favorites""",
            """there are 12 characters with special meanings: the backslash \, the caret ^, the dollar sign $, the period or dot ., the vertical bar or pipe symbol |, the question mark ?, the asterisk or star *, the plus sign +, the opening parenthesis (, the closing parenthesis ), and the opening square bracket [, the opening curly brace {, These special characters are often called "metacharacters".
""", """/usr/bin/java -> /Library/Java/JavaVirtualMachines/jdk1.7.0_25.jdk/Contents/Home/bin/java
""", """ls -l <whatever the /usr/bin/java symlink points to>
""", """method1 took 972 ms, result was 2
method2 took 1003 ms, result was 2
method3 took 66716 ms, result was 2""", """mvn -pl <module-name> -Dit.test=TestCircle#xyz integration-test
""", """a
b
c
""", """Whenever a new class instance is created, memory space is allocated
  for it with room for all the instance variables declared in the class
  type and all the instance variables declared in each superclass of the
  class type, including all the instance variables that may be hidden.
Just before a reference to the newly created object is returned as the
  result, the indicated constructor is processed to initialize the new
  object using the following procedure:"""
        ]
        cc = CodeContentClassification()
        for t in t_list:
            self.assertEqual(cc.Label_Text, cc.get_label(t))

    def test_all(self):
        cc = CodeContentClassification()
        trace_list = [
            """06-03 15:05:29.614: ERROR/AndroidRuntime(7737): java.lang.UnsupportedOperationException
06-03 15:05:29.614: ERROR/AndroidRuntime(7737):     at java.util.AbstractList.remove(AbstractList.java:645)
""", """java.sql.SQLException: No suitable driver found for jdbc:mysql://database/table
            at java.sql.DriverManager.getConnection(DriverManager.java:689)
            at java.sql.DriverManager.getConnection(DriverManager.java:247)
        """, """W/System.err(  901): javax.net.ssl.SSLException: Not trusted server certificate 
        W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.OpenSSLSocketImpl.startHandshake(OpenSSLSocketImpl.java:360) 
        W/System.err(  901):    at org.apache.http.conn.ssl.AbstractVerifier.verify(AbstractVerifier.java:92) 
        W/System.err(  901):    at org.apache.http.conn.ssl.SSLSocketFactory.connectSocket(SSLSocketFactory.java:321) 
        W/System.err(  901):    at org.apache.http.impl.conn.DefaultClientConnectionOperator.openConnection(DefaultClientConnectionOperator.java:129) 
        W/System.err(  901):    at org.apache.http.impl.conn.AbstractPoolEntry.open(AbstractPoolEntry.java:164) 
        W/System.err(  901):    at org.apache.http.impl.conn.AbstractPooledConnAdapter.open(AbstractPooledConnAdapter.java:119) 
        W/System.err(  901):    at org.apache.http.impl.client.DefaultRequestDirector.execute(DefaultRequestDirector.java:348) 
        W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:555) 
        W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:487) 
        W/System.err(  901):    at org.apache.http.impl.client.AbstractHttpClient.execute(AbstractHttpClient.java:465) 
        W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity.connect(MainActivity.java:129) 
        W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity.access$0(MainActivity.java:77) 
        W/System.err(  901):    at me.harrisonlee.test.ssl.MainActivity$2.run(MainActivity.java:49) 
        W/System.err(  901): Caused by: java.security.cert.CertificateException: java.security.InvalidAlgorithmParameterException: the trust anchors set is empty 
        W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.TrustManagerImpl.checkServerTrusted(TrustManagerImpl.java:157) 
        W/System.err(  901):    at org.apache.harmony.xnet.provider.jsse.OpenSSLSocketImpl.startHandshake(OpenSSLSocketImpl.java:355) 
        W/System.err(  901):    ... 12 more 
        W/System.err(  901): Caused by: java.security.InvalidAlgorithmParame
        """, """However, I get a NoSuchElementException (since there is no invocation of hasNext) Exception in thread "main" java.util.NoSuchElementException
        at java.util.AbstractList$Itr.next(AbstractList.java:364)
        at Main$$Lambda$1/1175962212.get(Unknown Source)
        at java.util.stream.StreamSpliterators$InfiniteSupplyingSpliterator$OfRef.tryAdvance(StreamSpliterators.java:1351)
        at java.util.Spliterator.forEachRemaining(Spliterator.java:326)
        at java.util.stream.ReferencePipeline$Head.forEach(ReferencePipeline.java:580)
        at Main.main(Main.java:20)""",
            """[INFO] --- maven-surefire-plugin:2.18.1:test (default-test) @ recorder ---
[INFO] Surefire report directory: /lhome/code/recorder/target/surefire-reports
[INFO] Using configured provider org.apache.maven.surefire.junitcore.JUnitCoreProvider
[INFO] parallel='none', perCoreThreadCount=true, threadCount=0, useUnlimitedThreads=false, threadCountSuites=0,     threadCountClasses=0, threadCountMethods=0, parallelOptimized=true
""", """Error: Could not find or load main class org.apache.maven.surefire.booter.ForkedBooter
        
        Results :
        
        Tests run: 0, Failures: 0, Errors: 0, Skipped: 0""", """[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test (default-test) on project recorder: Execution default-test of goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test failed: The forked VM terminated without properly saying goodbye. VM crash or System.exit called?
        """, """213
        
        
        40
        Recently coming to a new project, I'm trying to compile our source code. Everything worked fine yesterday, but today is another story.
        
        Every time I'm running mvn clean install on a module, once reaching the tests, it crashes into an error:
        
        [INFO] --- maven-surefire-plugin:2.18.1:test (default-test) @ recorder ---
        [INFO] Surefire report directory: /lhome/code/recorder/target/surefire-reports
        [INFO] Using configured provider org.apache.maven.surefire.junitcore.JUnitCoreProvider
        [INFO] parallel='none', perCoreThreadCount=true, threadCount=0, useUnlimitedThreads=false, threadCountSuites=0,     threadCountClasses=0, threadCountMethods=0, parallelOptimized=true
        """, """Error: Could not find or load main class org.apache.maven.surefire.booter.ForkedBooter
        
        Results :
        
        Tests run: 0, Failures: 0, Errors: 0, Skipped: 0
        and later on:
        
        [ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test (default-test) on project recorder: Execution default-test of goal org.apache.maven.plugins:maven-surefire-plugin:2.18.1:test failed: The forked VM terminated without properly saying goodbye. VM crash or System.exit called?
        I'm running on Debian 9 (Stretch) 64-bits with OpenJDK 1.8.0_181, Maven 3.5.4, working behind my company proxy which I configured in my ~/.m2/settings.xml.
        
        A strange thing it that the latest Surefire version is 2.22.1 if I remember correctly. I tried to specify the plugin version, but it does not get updated, otherwise there's no plugin version specification in any POM (parent, grand-parent or this one).
        
        I managed to force Maven to change the Surefire version to the latest, but now it's even worse:"""
        ]
        for t in trace_list:
            label = cc.get_label(t)
            if label != cc.Label_Stacktrace:
                print("a")
            self.assertEqual(cc.Label_Stacktrace, label)
        xml_list = [
            """<project>
          [...]
          <build>
            [...]
            <plugins>
              <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                  <source>1.8</source>
                  <target>1.8</target>
                </configuration>
              </plugin>
            </plugins>
            [...]
          </build>
          [...]
        </project>""", """<bean id="userLister" class="UserListerDB" />

        <bean class="SomeView">
            <property name="userLister" ref="userLister" />
        </bean>""", """<build>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <configuration>
                        <source>1.8</source>
                        <target>1.8</target>
                    </configuration>
                </plugin>
            </plugins>
        </build>""", """<!DOCTYPE html>
        <html lang="en">
            <head>
                <title>SO question 4112686</title>
                <script src="http://code.jquery.com/jquery-latest.min.js"></script>
                <script>
                    $(document).on("click", "#somebutton", function() { // When HTML DOM "click" event is invoked on element with ID "somebutton", execute the following function...
                        $.get("someservlet", function(responseText) {   // Execute Ajax GET request on URL of "someservlet" and execute the following function with Ajax response text...
                            $("#somediv").text(responseText);           // Locate HTML DOM element with ID "somediv" and set its text content with the response text.
                        });
                    });
                </script>
            </head>
            <body>
                <button id="somebutton">press here</button>
                <div id="somediv"></div>
            </body>
        </html>""", """
        {
          "applesDO" : [
            {
              "apple" : "Green Apple"
            },
            {
              "apple" : "Red Apple"
            }
          ]
        }"""
        ]
        for t in xml_list:
            label = cc.get_label(t)
            if label != cc.Label_XML_or_JSON:
                print("a")
            self.assertEqual(cc.Label_XML_or_JSON, label)
        num_list = ["""[7.0, 9.0, 5.0, 1.0, 3.0 ]""", """  PID      Vss      Rss      Pss      Uss  cmdline
  890   84456K   48668K   25850K   21284K  system_server
 1231   50748K   39088K   17587K   13792K  com.android.launcher2
  947   34488K   28528K   10834K    9308K  com.android.wallpaper
  987   26964K   26956K    8751K    7308K  com.google.process.gapps
  954   24300K   24296K    6249K    4824K  com.android.phone
  948   23020K   23016K    5864K    4748K  com.android.inputmethod.latin
  888   25728K   25724K    5774K    3668K  zygote
  977   24100K   24096K    5667K    4340K  android.process.acore
...
   59     336K     332K      99K      92K  /system/bin/installd
   60     396K     392K      93K      84K  /system/bin/keystore
   51     280K     276K      74K      68K  /system/bin/servicemanager
   54     256K     252K      69K      64K  /system/bin/debuggerd""",
                    """
                                SI     BINARY
  
                     0:        0 B        0 B
                    27:       27 B       27 B
                   999:      999 B      999 B
                  1000:     1.0 kB     1000 B
                  1023:     1.0 kB     1023 B
                  1024:     1.0 kB    1.0 KiB
                  1728:     1.7 kB    1.7 KiB
                110592:   110.6 kB  108.0 KiB
               7077888:     7.1 MB    6.8 MiB
             452984832:   453.0 MB  432.0 MiB
           28991029248:    29.0 GB   27.0 GiB
         1855425871872:     1.9 TB    1.7 TiB
   9223372036854775807:     9.2 EB    8.0 EiB   (Long.MAX_VALUE)
  """, """Test1 Times (ms)           Test2 Times (ms)
----------------           ----------------
           187                          0
           203                          0
           203                          0
           188                          0
           188                          0
           187                          0
           203                          0
           188                          0
           188                          0
           203                          0""", """999199.1231231235 == 999199.1231231236 // true
1.03 - 0.41 // 0.6200000000000001"""
                    ]
        for t in num_list:
            label = cc.get_label(t)
            if label != cc.Label_Number:
                print("a")
            self.assertEqual(cc.Label_Number, label)
        code_list = [
            """ArrayList aList = new ArrayList();

//Add elements to ArrayList object
aList.add("1");
aList.add("2");
aList.add("3");
aList.add("4");
aList.add("5");

while (aList.listIterator().hasPrevious())
  Log.d("reverse", "" + aList.listIterator().previous());""",
            """
            Collections.reverse(aList);
            """,

            """Field f = obj.getClass().getDeclaredField("stuffIWant"); //NoSuchFieldException
f.setAccessible(true);
Hashtable iWantThis = (Hashtable) f.get(obj); //IllegalAccessException
""", """org.hamcrest.Matchers.*
org.hamcrest.CoreMatchers.*
org.junit.*
org.junit.Assert.*
org.junit.Assume.*
org.junit.matchers.JUnitMatchers.*""", """obj.getClass().getDeclaredField("misspelled"); //will throw NoSuchFieldException
""", """File f = new File(filePathString);
if(f.exists() && !f.isDirectory()) { 
    // do something
}
""", """public class SomeView {
    private UserLister userLister;

    public void render() {
        List<User> users = userLister.getUsers();
        view.render(users);
    }
}""", """public class Test {
    int value;


    public int getValue() {
        return value;
    }

    public void reset() {
        value = 0;
    }

    // Calculates without exception
    public void method1(int i) {
        value = ((value + i) / i) << 1;
        // Will never be true
        if ((i & 0xFFFFFFF) == 1000000000) {
            System.out.println("You'll never see this!");
        }
    }

    // Could in theory throw one, but never will
    public void method2(int i) throws Exception {
        value = ((value + i) / i) << 1;
        // Will never be true
        if ((i & 0xFFFFFFF) == 1000000000) {
            throw new Exception();
        }
    }

    // This one will regularly throw one
    public void method3(int i) throws Exception {
        value = ((value + i) / i) << 1;
        // i & 1 is equally fast to calculate as i & 0xFFFFFFF; it is both
        // an AND operation between two integers. The size of the number plays
        // no role. AND on 32 BIT always ANDs all 32 bits
        if ((i & 0x1) == 1) {
            throw new Exception();
        }
    }

    public static void main(String[] args) {
        int i;
        long l;
        Test t = new Test();

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            t.method1(i);
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method1 took " + l + " ms, result was " + t.getValue()
        );

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            try {
                t.method2(i);
            } catch (Exception e) {
                System.out.println("You'll never see this!");
            }
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method2 took " + l + " ms, result was " + t.getValue()
        );

        l = System.currentTimeMillis();
        t.reset();
        for (i = 1; i < 100000000; i++) {
            try {
                t.method3(i);
            } catch (Exception e) {
                // Do nothing here, as we will get here
            }
        }
        l = System.currentTimeMillis() - l;
        System.out.println(
            "method3 took " + l + " ms, result was " + t.getValue()
        );
    }
}""", """if((x & 4294967295LL) == 0)
    x >>= 32;
if((x & 65535) == 0)
    x >>= 16;
if((x & 255) == 0)
    x >>= 8;
if((x & 15) == 0)
    x >>= 4;
if((x & 3) == 0)
    x >>= 2;""", """typedef signed long long int int64;

int start[1024] =
{1,3,1769,5,1937,1741,7,1451,479,157,9,91,945,659,1817,11,
1983,707,1321,1211,1071,13,1479,405,415,1501,1609,741,15,339,1703,203,
129,1411,873,1669,17,1715,1145,1835,351,1251,887,1573,975,19,1127,395,
1855,1981,425,453,1105,653,327,21,287,93,713,1691,1935,301,551,587,
257,1277,23,763,1903,1075,1799,1877,223,1437,1783,859,1201,621,25,779,
1727,573,471,1979,815,1293,825,363,159,1315,183,27,241,941,601,971,
385,131,919,901,273,435,647,1493,95,29,1417,805,719,1261,1177,1163,
1599,835,1367,315,1361,1933,1977,747,31,1373,1079,1637,1679,1581,1753,1355,
513,1539,1815,1531,1647,205,505,1109,33,1379,521,1627,1457,1901,1767,1547,
1471,1853,1833,1349,559,1523,967,1131,97,35,1975,795,497,1875,1191,1739,
641,1149,1385,133,529,845,1657,725,161,1309,375,37,463,1555,615,1931,
1343,445,937,1083,1617,883,185,1515,225,1443,1225,869,1423,1235,39,1973,
769,259,489,1797,1391,1485,1287,341,289,99,1271,1701,1713,915,537,1781,
1215,963,41,581,303,243,1337,1899,353,1245,329,1563,753,595,1113,1589,
897,1667,407,635,785,1971,135,43,417,1507,1929,731,207,275,1689,1397,
1087,1725,855,1851,1873,397,1607,1813,481,163,567,101,1167,45,1831,1205,
1025,1021,1303,1029,1135,1331,1017,427,545,1181,1033,933,1969,365,1255,1013,
959,317,1751,187,47,1037,455,1429,609,1571,1463,1765,1009,685,679,821,
1153,387,1897,1403,1041,691,1927,811,673,227,137,1499,49,1005,103,629,
831,1091,1449,1477,1967,1677,697,1045,737,1117,1737,667,911,1325,473,437,
1281,1795,1001,261,879,51,775,1195,801,1635,759,165,1871,1645,1049,245,
703,1597,553,955,209,1779,1849,661,865,291,841,997,1265,1965,1625,53,
1409,893,105,1925,1297,589,377,1579,929,1053,1655,1829,305,1811,1895,139,
575,189,343,709,1711,1139,1095,277,993,1699,55,1435,655,1491,1319,331,
1537,515,791,507,623,1229,1529,1963,1057,355,1545,603,1615,1171,743,523,
447,1219,1239,1723,465,499,57,107,1121,989,951,229,1521,851,167,715,
1665,1923,1687,1157,1553,1869,1415,1749,1185,1763,649,1061,561,531,409,907,
319,1469,1961,59,1455,141,1209,491,1249,419,1847,1893,399,211,985,1099,
1793,765,1513,1275,367,1587,263,1365,1313,925,247,1371,1359,109,1561,1291,
191,61,1065,1605,721,781,1735,875,1377,1827,1353,539,1777,429,1959,1483,
1921,643,617,389,1809,947,889,981,1441,483,1143,293,817,749,1383,1675,
63,1347,169,827,1199,1421,583,1259,1505,861,457,1125,143,1069,807,1867,
2047,2045,279,2043,111,307,2041,597,1569,1891,2039,1957,1103,1389,231,2037,
65,1341,727,837,977,2035,569,1643,1633,547,439,1307,2033,1709,345,1845,
1919,637,1175,379,2031,333,903,213,1697,797,1161,475,1073,2029,921,1653,
193,67,1623,1595,943,1395,1721,2027,1761,1955,1335,357,113,1747,1497,1461,
1791,771,2025,1285,145,973,249,171,1825,611,265,1189,847,1427,2023,1269,
321,1475,1577,69,1233,755,1223,1685,1889,733,1865,2021,1807,1107,1447,1077,
1663,1917,1129,1147,1775,1613,1401,555,1953,2019,631,1243,1329,787,871,885,
449,1213,681,1733,687,115,71,1301,2017,675,969,411,369,467,295,693,
1535,509,233,517,401,1843,1543,939,2015,669,1527,421,591,147,281,501,
577,195,215,699,1489,525,1081,917,1951,2013,73,1253,1551,173,857,309,
1407,899,663,1915,1519,1203,391,1323,1887,739,1673,2011,1585,493,1433,117,
705,1603,1111,965,431,1165,1863,533,1823,605,823,1179,625,813,2009,75,
1279,1789,1559,251,657,563,761,1707,1759,1949,777,347,335,1133,1511,267,
833,1085,2007,1467,1745,1805,711,149,1695,803,1719,485,1295,1453,935,459,
1151,381,1641,1413,1263,77,1913,2005,1631,541,119,1317,1841,1773,359,651,
961,323,1193,197,175,1651,441,235,1567,1885,1481,1947,881,2003,217,843,
1023,1027,745,1019,913,717,1031,1621,1503,867,1015,1115,79,1683,793,1035,
1089,1731,297,1861,2001,1011,1593,619,1439,477,585,283,1039,1363,1369,1227,
895,1661,151,645,1007,1357,121,1237,1375,1821,1911,549,1999,1043,1945,1419,
1217,957,599,571,81,371,1351,1003,1311,931,311,1381,1137,723,1575,1611,
767,253,1047,1787,1169,1997,1273,853,1247,413,1289,1883,177,403,999,1803,
1345,451,1495,1093,1839,269,199,1387,1183,1757,1207,1051,783,83,423,1995,
639,1155,1943,123,751,1459,1671,469,1119,995,393,219,1743,237,153,1909,
1473,1859,1705,1339,337,909,953,1771,1055,349,1993,613,1393,557,729,1717,
511,1533,1257,1541,1425,819,519,85,991,1693,503,1445,433,877,1305,1525,
1601,829,809,325,1583,1549,1991,1941,927,1059,1097,1819,527,1197,1881,1333,
383,125,361,891,495,179,633,299,863,285,1399,987,1487,1517,1639,1141,
1729,579,87,1989,593,1907,839,1557,799,1629,201,155,1649,1837,1063,949,
255,1283,535,773,1681,461,1785,683,735,1123,1801,677,689,1939,487,757,
1857,1987,983,443,1327,1267,313,1173,671,221,695,1509,271,1619,89,565,
127,1405,1431,1659,239,1101,1159,1067,607,1565,905,1755,1231,1299,665,373,
1985,701,1879,1221,849,627,1465,789,543,1187,1591,923,1905,979,1241,181};

bool bad255[512] =
{0,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,
 1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,
 0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,
 1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,
 1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,
 1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,
 1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,
 1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
 0,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,
 1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,
 0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,
 1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,
 1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,
 1,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,
 1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,
 1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,
 0,0};

inline bool square( int64 x ) {
    // Quickfail
    if( x < 0 || (x&2) || ((x & 7) == 5) || ((x & 11) == 8) )
        return false;
    if( x == 0 )
        return true;

    // Check mod 255 = 3 * 5 * 17, for fun
    int64 y = x;
    y = (y & 4294967295LL) + (y >> 32);
    y = (y & 65535) + (y >> 16);
    y = (y & 255) + ((y >> 8) & 255) + (y >> 16);
    if( bad255[y] )
        return false;

    // Divide out powers of 4 using binary search
    if((x & 4294967295LL) == 0)
        x >>= 32;
    if((x & 65535) == 0)
        x >>= 16;
    if((x & 255) == 0)
        x >>= 8;
    if((x & 15) == 0)
        x >>= 4;
    if((x & 3) == 0)
        x >>= 2;

    if((x & 7) != 1)
        return false;

    // Compute sqrt using something like Hensel's lemma
    int64 r, t, z;
    r = start[(x >> 3) & 1023];
    do {
        z = x - r * r;
        if( z == 0 )
            return true;
        if( z < 0 )
            return false;
        t = z & (-z);
        r += (z & t) >> 1;
        if( r > (t  >> 1) )
            r = t - r;
    } while( t <= (1LL << 33) );

    return false;
}"""
        ]
        for t in code_list:
            label = cc.get_label(t)
            if label != cc.Label_Code:
                print("a")
            self.assertEqual(cc.Label_Code, label)

    def load_json_test_file(self):
        Label_DATA_DIR = os.path.join(ROOT_DIR, 'label_data')
        json_file_path = Path(Label_DATA_DIR) / "so_content_label.json"
        res_list = []
        with open(str(json_file_path), 'r', encoding='UTF-8') as f:
            for jsonstr in f.readlines():
                # 将josn字符串转化为dict字典
                jsonstr = json.loads(jsonstr)
                res_list.append(jsonstr)
        return res_list

    def test_from_json(self):
        cc = CodeContentClassification()

        data = self.load_json_test_file()
        for each in data:
            label = each["labels"][0]
            text = each["text"]
            # if text.find("synchronized (mon) { mon.notify(); }")<0:
            #     continue
            predict_label = cc.label_code_2_name[cc.get_label(text)]
            if label != predict_label:
                print("predict_label:" + predict_label, "label:" + label)
                print(text)
                # self.assertEqual(predict_label, label)
