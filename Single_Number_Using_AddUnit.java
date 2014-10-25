public class Solution {
    //m需要的存储位数
    int ceil_log(int m) {
    	if(m < 2) {
    		throw new RuntimeException("invalid input");
    	}
    	int k = 0;
    	int s = 1;
    	while(s < m) {
    		s *= 2;
    		k++;
    	}
    	return k;
    }
    //普通加法器
    void addUnit_normal(int[] s, int x) {
    	int f = x;
    	for(int i = 0; i < s.length; i++) {
    		int f_next = s[i] & f;
    		s[i] ^= f;
    		f = f_next;
    	}
    }
    //行波加法器
    void addUnit_travelWave(int[] s, int x) {
        int w = s[0];
    	s[0] ^= x;
    	for(int i = 1; i < s.length; i++) {
    		int w_next = w & s[i];
    		s[i] ^= (x & w);
    		w = w_next;
    	}
    }
    
    //mod(n)运算
    void modUnit(int[] s, int m) {
    	//==m的标记位
    	int flag = (m % 2 == 1) ? s[0] : ~s[0];
    	m /= 2;
    	for(int i = 1; i < s.length; i++) {
    		flag &= (m % 2 == 1) ? s[i] : ~s[i];
    		m /= 2;
    	}
    	//根据标记位归0
    	for(int i = 0; i < s.length; i++) {
    		s[i] &= ~flag;
    	}
    }
    
    //mod(n)加法器
    void modAddUnit(int[]s, int x, int m) {
    	addUnit_travelWave(s, x);
    	modUnit(s, m);
    }
    
    public int singleNumber(int[] numbers, int m) {
    	if(m < 2) {
    		throw new RuntimeException("invalid input");
    	}
    	//m的计数器
    	int k = ceil_log(m);
        int[] s = new int[k];
        
        for(int x : numbers) {
        	modAddUnit(s, x, m);
        }
        
        return s[0];
    }
    
    public int singleNumber(int[] numbers) {
    	return singleNumber(numbers, 3);
    }
}
