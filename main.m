% Initial Data Read
schools = csvread('schoolsviolet.csv');
roadscommutes = csvread('roadscommutesviolet.csv');
roads_id = roadscommutes(:,1);
schools_id = schools(:,1);

% Formatting Data into Matrices-----------------------------------------
% E is binary matrix of roads and which SES category they fall in, R x 3
E = roadscommutes(:,5:7);
% T is the transit times R x S
T = roadscommutes(:,9:end);
% Pr is the population of each road segment
Pr = roadscommutes(:,2);
% C is the school capacity for each school
C = (schools(:,5)) * 1.25;
%Proportions of each SES group in schools
Pm =schools(:,2:4);
%Use for moderate SES weight
Wm = ((Pm-(1/3))/4)+1;
%Use for strong SES weight
%Wm = ((Pm-(1/3))/4)+1;
%Use for no SES weight - commute only
%Wm = ones(S,3);

%Dimensions scalars
R = size(T,1);
S = size(T,2);

% Matrix Manipulations
Pr3 = repmat(Pr,1,3);
PrPrime = repmat(Pr,1,R);
%----------------------------------------------------------------------


%A and b creation------------------------------------------------------
A = zeros([S,(R*S)]);
for i = 1:S
    for j = 1:R
        A(i,((i-1)*R)+j) = Pr(j);
    end
end
b = C;
%----------------------------------------------------------------------

%Aeq and beq creation--------------------------------------------------
IR = eye(R);
Aeq = repmat(IR,1,S);
%beq
one = [1];
beq = repmat(one,[1,R]);
%----------------------------------------------------------------------


%upper and lower bound-------------------------------------------------
x = 1:(R*S);
lb = zeros([R*S,1]);
ub = ones([R*S,1]);
%----------------------------------------------------------------------


%Objective Function -----------------------------------------------------
%W tiled so that rows along the diagonal are each schools 3 weight values
W = zeros((S*3),S); 
for i = 1:S
    for j = 1:3
        W(((i-1)*3) + j, i) = Wm(i,j);
    end
end
% Etile of the E matrix repeated S times along the columns)
Etile = repmat(E,1,S);
Tthrees = reshape(repmat(reshape(T',[],1),1,3)',[],size(T,1))';
ET = Etile.*Tthrees;
ETW = ET*W;
PrrepS = repmat(Pr,1,S);
F = ETW.*PrrepS;
ObjF = zeros([1,R*S]);
for i = 1:S
    for j = 1:R
        ObjF(1,((i-1)*R) + j) = F(j,i);
    end
end
%----------------------------------------------------------------------


% Linear Programming Call----------------------------------------------
%assignments = intlinprog(ObjF,x, A,b, Aeq, beq,lb, ub);
assignments = linprog(ObjF, A, b, Aeq, beq, lb, ub);
%----------------------------------------------------------------------

%re-formatting assignments output--------------------------------------
ass_matrix_lp = zeros([R,S]);
for i = 1:S
    for j = 1:R
        ass_matrix_lp(j,i) = (assignments(((i-1)*R)+j));
    end
end

% find the maximum assignment of values
ass_matrix= zeros([R,S]);
AMax = max(ass_matrix_lp,[],2); 
% finds the minimum commute for a road segment
[TMin, TminInd] = min(T, [], 2);
for i = 1:S
    for j = 1:R
        if(M(j) > 0.5)
            ass_matrix(j,i) = 1;
        end
    end
end
assign_sum = sum(ass_matrix, 2);
for j = 1:R
    if assign_sum == 0;
        ass_matrix(j,TminInd(j)) = 1;
    end
end
id_ass_num = ass_matrix * schools_id;
%----------------------------------------------------------------------


%Functions to calculate summary statistics on the assignment-----------
clear enrollments;
clear commute_avgs;
clear commute_avg;
clear SES_props;
clear high_pov_count;
%calculates the assigned enrollment to each school
enrollments = enrollments( ass_matrix, Pr, S);
%average commute time for each school
commute_avgs = commute_avgs(ass_matrix, T, Pr, S);
%total average commute time
commute_avg = commute_avg(ass_matrix, T, Pr, S);
SES_props = SES_props(ass_matrix, E, Pr, S);
%counts the number of schools that still have over 90% of their students
    %in the low SES catate
high_pov_count = high_pov_count(ass_matrix, E, Pr, S );
%----------------------------------------------------------------------