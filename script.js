document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const fairyCard = document.getElementById('fairy-card');

    const fairyData = {
        name1: ['靄', '泥', '泡', '幻', '静寂', '忘れ', '沈黙', '憂い', '水鏡', '夜光'],
        name2: ['の精', 'の雫', 'の影', 'の囁き', 'の調べ', 'の主', 'の番人', 'の灯火', 'の迷子', 'の踊り子'],
        alias1: ['Haze', 'Mire', 'Bubble', 'Phantom', 'Silence', 'Oblivion', 'Hush', 'Sorrow', 'Aqua-Mirror', 'Glimmer'],
        alias2: ['Sprite', 'Droplet', 'Shade', 'Whisper', 'Melody', 'Master', 'Warden', 'Light', 'Wanderer', 'Dancer'],
        feature: [
            '体は常に湿った苔で覆われている。',
            '月光を浴びると、体の色が七色に変化する。',
            '人の記憶を少しずつ食べて生きている。',
            '笑い声が、水底から泡が立つような音に似ている。',
            '古い書物のインクの匂いがする。',
            'その姿を見た者は、最も大切な思い出を一つ忘れてしまう。',
            '体から零れ落ちる雫は、触れると温かい。',
            '常に悲しげな表情を浮かべているが、本当は喜んでいる。',
            '沼の底にある美しいものだけを集めている。',
            '言葉を話さず、身振り手振りだけで意思を伝える。'
        ],
        behavior: [
            '誰かが沼のほとりで深く考え事をしていると、そっと現れる。',
            '沼に捨てられたものに新たな命を吹き込む。',
            '夜通し、水面で一人静かに踊り続ける。',
            '迷い込んだ人間を、沼のさらに奥深くへと誘う。',
            '沼の生き物たちの声を聴き、その代弁者となる。',
            '満月の夜にだけ、美しい歌を歌う。',
            '自分の姿を隠すのが得意で、めったに人前に現れない。',
            '人間が失くしたものを、こっそり元の場所に戻してあげる。',
            '沼の透明度を保つために、毎日せっせと不純物を取り除いている。',
            '気に入った人間の夢の中に現れて、助言を与える。'
        ],
        location: [
            '忘れ去られた公園の池。',
            '雨上がりの、アスファルトにできた水たまり。',
            '古書店の、インクと紙の匂いが充満した一角。',
            '深夜の、誰もいないプログラマーのデスクの上。',
            '長い間使われていない、蛇口から滴る水の音だけが響くバスルーム。',
            'SNSの、延々と続くタイムラインの底。',
            '何時間も同じ曲をリピート再生しているヘッドフォンの中。',
            '閉館後の美術館、静まり返った展示室。',
            '膨大な資料に埋もれた、研究室の片隅。',
            'クリアできないゲームの、同じステージの中。'
        ],
        symbolism: [
            '「忘却」と「再生」',
            '「孤独」と「探求」',
            '「創造」と「混沌」',
            '「過去」と「未来」',
            '「喪失」と「発見」',
            '「静寂」と「内なる声」',
            '「執着」と「解放」',
            '「現実」と「夢」',
            '「秩序」と「無秩序」',
            '「始まり」と「終わり」'
        ]
    };

    // Simple Katakana transliteration
    const toKatakana = {
        'Haze': 'ヘイズ', 'Mire': 'マイア', 'Bubble': 'バブル', 'Phantom': 'ファントム', 'Silence': 'サイレンス', 
        'Oblivion': 'オブリビオン', 'Hush': 'ハッシュ', 'Sorrow': 'ソロー', 'Aqua-Mirror': 'アクアミラー', 'Glimmer': 'グリマー',
        'Sprite': 'スプライト', 'Droplet': 'ドロップレット', 'Shade': 'シェイド', 'Whisper': 'ウィスパー', 'Melody': 'メロディ',
        'Master': 'マスター', 'Warden': 'ウォーデン', 'Light': 'ライト', 'Wanderer': 'ワンダラー', 'Dancer': 'ダンサー'
    };

    function getRandomIndex(arr) {
        return Math.floor(Math.random() * arr.length);
    }

    generateBtn.addEventListener('click', () => {
        const index = getRandomIndex(fairyData.name1);
        
        const name1 = fairyData.name1[index];
        const name2 = fairyData.name2[index];
        const fairyName = `${name1}${name2}`;

        const alias1 = fairyData.alias1[index];
        const alias2 = fairyData.alias2[index];
        const fairyAlias = `${toKatakana[alias1]}・${toKatakana[alias2]}`;

        document.getElementById('fairy-name').textContent = fairyName;
        document.getElementById('fairy-alias').textContent = fairyAlias;
        document.getElementById('fairy-feature').textContent = fairyData.feature[getRandomIndex(fairyData.feature)];
        document.getElementById('fairy-behavior').textContent = fairyData.behavior[getRandomIndex(fairyData.behavior)];
        document.getElementById('fairy-location').textContent = fairyData.location[getRandomIndex(fairyData.location)];
        document.getElementById('fairy-symbolism').textContent = fairyData.symbolism[getRandomIndex(fairyData.symbolism)];

        fairyCard.classList.remove('hidden');
    });
});
