/*
 * @Author: zhangqj
 * @Date: 2021-05-29 20:38:50
 * @LastEditTime: 2021-05-30 01:27:32
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /Toy/RepGame.cpp
 */
#include<iostream>
#include <stdlib.h> 
#include <time.h> 
#include <cstdlib>
using namespace std;
#define MaxPlayer 100
#define Rational 0
#define Random 1

#define UpUp 0
#define UpDown 1
#define DownUp 2
#define DownDown 3
// The route is below
//              A                           //
//        1   / | \   n                     //
//           /  |  \                        //
//          S   |c  D                       //
//           \  |  /                        //
//        n   \ | /   1                     //
//              B                           //
//                                          //
int RepetitionCounter, NumRandom, NumRational ;
double Constant ;
long long ChooseFirstDown,ChooseSecondUp;
long long RandomActions[MaxPlayer],RationalActions[MaxPlayer];
long long RandomCost[MaxPlayer],RationalCost[MaxPlayer];



int RealRandomNum(int mod){
    srand((int)time(0));
    return rand() % mod;
}

class ActionRecord{
public:
    ActionRecord( ):FirstUp( 0 ) , FirstDown( 0 ),
                    SecondUp( 0 ),SecondDown( 0 ){}
    void ActionFirstUp(){ FirstUp++; }
    void ActionFirstDown(){ FirstDown++; }
    void ActionSecondUp(){ SecondUp++; }
    void ActionSecondDown(){ SecondDown++; }
    double FirstUpRate(){ 
        if (FirstUp == FirstDown) return 0.5;
        return double( FirstUp / (FirstUp+FirstDown) );}
    double FirstDownRate(){ 
        if (FirstUp == FirstDown) return 0.5;
        return double( FirstDown / (FirstUp+FirstDown) );}
    double SecondUpRate(){
        if (SecondUp == SecondDown) return 0.5;
        return double( SecondUp / (SecondUp+SecondDown) );}
    double SecondDownRate(){ 
        if (SecondUp == SecondDown) return 0.5;
        return double( SecondDown / (SecondUp+SecondDown) );}

private:
    int FirstUp;int FirstDown;
    int SecondUp;int SecondDown;
};
ActionRecord RandomRecord[MaxPlayer] ,RationalRecord[MaxPlayer];
// The route is below
//              A                           //
//        1   / | \   n                     //
//           /  |  \                        //
//          S   |c  D                       //
//           \  |  /                        //
//        n   \ | /   1                     //
//              B                           //
//                                          //

int RationalAction(int id){
    int NumDown =0,NumUp=0;
    int action;
    for(int i = 0; i < NumRandom;i++){
        // First Action
        if (RandomRecord[i].FirstDownRate() > 0.5) NumDown++;
        else if (RandomRecord[i].FirstDownRate() == 0.5) NumDown += RealRandomNum(2);
        // Second Action
        if (RandomRecord[i].SecondUpRate() > 0.5) NumUp++;
        else if (RandomRecord[i].SecondUpRate() == 0.5) NumUp += RealRandomNum(2);

    }
    
    for(int i = 0; i < NumRational;i++){
        // don't take player herself into consideration
        if (i == id) continue;
        // First Action

        if (RationalRecord[i].FirstDownRate() > 0.5) NumDown++;
        else if (RationalRecord[i].FirstDownRate() == 0.5) NumDown += RealRandomNum(2);

        if (RationalRecord[i].SecondUpRate() > 0.5) NumUp++;
        else if (RationalRecord[i].SecondUpRate() == 0.5) NumUp += RealRandomNum(2);
    }
 

    int TotalPlayer = NumRandom + NumRational ;
    
    double Expection[4];
    Expection[UpUp] = 1.1 +  (NumUp+1)/TotalPlayer;
    Expection[UpDown]= 1.1 + Constant + 1.1;
    Expection[DownUp]= (NumDown+1)/TotalPlayer + Constant + (NumUp+1)/TotalPlayer;
    Expection[DownDown]= (NumDown+1)/TotalPlayer + 1.1;
    int MinExpection = 0,BestResponce = 0;
    for(int i = 0 ; i < 4; i++){
        if (MinExpection>Expection[i]){
            MinExpection = Expection[i];
            BestResponce = i;
        }else if  (MinExpection == Expection[i]){
            if (RealRandomNum(2)) BestResponce = i;
        }
    }
    RationalActions[id] = BestResponce;
    return BestResponce;
}
int RandomAction(int id){
    return RandomActions[id] = RealRandomNum(4);
}

// The route is below
//              A                           //
//        1   / | \   n                     //
//           /  |  \                        //
//          S   |c  D                       //
//           \  |  /                        //
//        n   \ | /   1                     //
//              B                           //
//                                          //
double CostSpace[4];
void CalCost(){
    double CostofSB = ChooseFirstDown/(NumRandom+NumRational);
    double CostofAD = ChooseSecondUp/(NumRandom+NumRational);
    CostSpace[UpUp] = 1.1 + CostofAD;
    CostSpace[UpDown] = 1.1 + Constant + 1.1;
    CostSpace[DownUp] =CostofSB+ Constant + CostofAD;
    CostSpace[DownDown] = CostofSB + 1.1;
}

class Player{
public:
    Player(){}
    void Set(int type,int id){ Type = type;Id = id;}
    int Action(){
        int ans = 0;

        if (Type == Random) ans = RandomAction(Id);
        else ans = RationalAction(Id);
        switch (ans)
        {
            case UpUp:
                ChooseSecondUp++;
                break;
            case DownUp:
                ChooseFirstDown++;
                ChooseSecondUp++;
                break;
            case DownDown:
                ChooseFirstDown++;
                break;
            default:
                break;
        }
        return ans;
    }
    void UpdateData(){
        // update the record and cost
        if (Type == Random){
            // update the record
            switch (RandomActions[Id])
            {
                case UpUp:
                    RandomRecord[Id].ActionFirstUp(),RandomRecord[Id].ActionSecondUp();
                    break;
                case UpDown:
                    RandomRecord[Id].ActionFirstUp(),RandomRecord[Id].ActionSecondDown();
                    break;
                case DownUp:
                    RandomRecord[Id].ActionFirstDown(),RandomRecord[Id].ActionSecondUp();
                    break;
                case DownDown:
                    RandomRecord[Id].ActionFirstDown(),RandomRecord[Id].ActionSecondDown();
                    break;
            }
            // store cost
            RandomCost[Id] += CostSpace[RandomActions[Id]];
            // reset result
            RandomActions[Id] = 0;
        }else{
            // update the record
            switch (RationalActions[Id])
            {
                case UpUp:
                    RationalRecord[Id].ActionFirstUp(),RationalRecord[Id].ActionSecondUp();
                    break;
                case UpDown:
                    RationalRecord[Id].ActionFirstUp(),RationalRecord[Id].ActionSecondDown();
                    break;
                case DownUp:
                    RationalRecord[Id].ActionFirstDown(),RationalRecord[Id].ActionSecondUp();
                    break;
                case DownDown:
                    RationalRecord[Id].ActionFirstDown(),RationalRecord[Id].ActionSecondDown();
                    break;
            }
            // store cost
            RationalCost[Id] += CostSpace[RationalActions[Id]];
            // reset result
            RationalActions[Id] = 0;
        }
    }
    void ShowData(){
        if (Type == Random){
            cout<<"Random Player"<<Id<<"'s Result:"<<endl;
            cout<<"The average cost is "<< RandomCost[Id]/RepetitionCounter<<endl;
        }
        else{ 
            cout<<"Rational Player"<<Id<<"'s Result:"<<endl;
            cout<<"The average cost is "<< RationalCost[Id]/RepetitionCounter<<endl;
        }
    }
private:
    int Type;//Type of Player
    int Id;
};




void PlayGame(int RepCount,int NumRandom,int NumRational){
    // init 
    Player RandomPlayer[NumRandom],RationalPlayer[NumRational];
    // First Round
    // Random Player Random choose
    for (int i = 0; i < NumRandom; i++){
        RandomPlayer[i].Set(Random,i);
        RandomPlayer[i].Action();
    }
    // RationalPlayer Rational choose

    for (int i = 0; i < NumRational; i++){
        RationalPlayer[i].Set(Rational,i);
        RationalPlayer[i].Action();
    }
    CalCost();
    for (int i = 0; i < NumRandom; i++){
        RandomPlayer[i].UpdateData();
    }
    for (int i = 0; i < NumRational; i++){
        RationalPlayer[i].UpdateData();
    }

    //Loop to play
    for(int i = 1 ; i < RepCount ; i++){
        ChooseFirstDown = 0;
        ChooseSecondUp = 0;
        // decide action
        for (int i = 0; i < NumRandom; i++){
            RandomPlayer[i].Action();
        }
        for (int i = 0; i < NumRational; i++){
            RationalPlayer[i].Action();
        }
        // cal the cost and update data
        CalCost();
        for (int i = 0; i < NumRandom; i++){
            RandomPlayer[i].UpdateData();
        }
        for (int i = 0; i < NumRational; i++){
            RationalPlayer[i].UpdateData();
        }
    }

    for (int i = 0; i < NumRandom; i++){
            RandomPlayer[i].ShowData();
    }
    for (int i = 0; i < NumRational; i++){
            RationalPlayer[i].ShowData();
    }


}




int main(int argc, char ** argv){
    // passing args like repetition counts,number of random players ,rational players,constant of middle express way
    RepetitionCounter = atoi(argv[1]);
    NumRandom = atoi(argv[2]);
    NumRational= atoi(argv[3]);
    Constant = atof(argv[4]);
    PlayGame(RepetitionCounter,NumRandom,NumRational);
    return 0;
}
