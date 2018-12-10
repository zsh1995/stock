let pieces_3phase = [{
            lte:0,
            color: '#eee'
        },{
            gt: 0,
            lte: 1,
            color: '#cc33ee' 
        }, {
            gt: 1,
            lte: 2,
            color: '#096'
        }, {
            gt: 2,
            lte: 3,
            color: '#ff9933'
        }]
let pieces_6phase = [{
                    lte:0,
                    color: '#eee'
                },{
                    gt: 0,
                    lte: 1,
                    color: '#ff9933' 
                }, {
                    gt: 1,
                    lte: 2,
                    color: '#096'
                }, {
                    gt: 2,
                    lte: 3,
                    color: '#660099'
                }, {
                    gt: 3,
                    lte: 4,
                    color: '#ff9933'
                }, {
                    gt: 4,
                    lte: 5,
                    color: '#096'
                }, {
                    gt: 5,
                    color: '#660099'
                }]
let positive_negative = [{
    gt: 0,
    color: "#ec0000"
},{
    lte:0,
    color: "#00da3c"
}]
let pieces_peek = [{
    gt:0,
    lte: 1,
    color: '#ff9933'
},{
    gt:1,
    lte: 2,
    color: '#096'
}]
let pieces_map = {
    'state' : pieces_6phase,
    'unacross': pieces_3phase,
    'peek' : pieces_peek,
    'postive_negative': positive_negative
}
