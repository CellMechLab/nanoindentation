import Fie.*
import dhaliwal_rau.*

fname='20200402_RosFake'
nu1 = 0.5;
nu2 = 0.5;
r = 3e-6;
d = 3e-6;

std_ND=0.5;
rand_around0_vary1=0.5*randn(1, 100);
basevalue_E1=1e4;
variation_E1=0.5e4;
basevalue_E2=1e3;
variation_E2=0.5e3;
basevalue_h=150e-9;
variation_h=75e-9;
noiselevel=500e-12; %pN

rand_E1=basevalue_E1+0.5*randn(1, 100)*variation_E1;
rand_E2=basevalue_E2+0.5*randn(1,100)*variation_E2;
rand_h=basevalue_h+0.5*randn(1,100)*variation_h;
for i=1:length(rand_E1)
    E1=rand_E1(i);
    E2=rand_E2(i);
    h=rand_h(i);
    if E1<=0
        E1=basevalue_E1+2*(rand(1,1)+0.5)*variation_E1;
        rand_E1(i)=E1;
        disp('E1 negative, set to', E1);
    elif E2<=0
        E2 = basevalue_E2 + 2 * (rand(1, 1) + 0.5) * variation_E2;
        rand_E2(i) = E2;
        disp('E2 negative, set to', E2);
    elif h<=0
        h = basevalue_h + 2 * (rand(1, 1) + 0.5) * variation_h;
        rand_h(i) = h;
        disp('h negative, set to', h);
    end
    fc = dhaliwal_rau(E1,nu1,E2,nu2,h,r,1,'sphere',0:d/1000:d);
    indent= fc.ext(1:end,1)
    force= fc.ext(:,2)

    %save curve to txt.file
    towrite=[indent; force];
    fname_i = strcat(fname,'_', string(i),'.txt');
    fileID = fopen(fname_i,'w');
    fprintf(fileID,'%6s %6s %6s %12.8f %12.8f %12.8f\n','E1','E2', 'h', E1, E2, h);
    fprintf(fileID,'%6s %12s\n','x','F');
    fprintf(fileID,'%6.2f %12.8f\n',A);
    fclose(fileID);

    % add random noise to curve
    noise=2*(rand(1,length(force))-0.5)*noiselevel
    forcewithnoise=[]
    for j=1:length(force)
        forcewithnoise(j)=force(j)+noise(j)
    end

    % save curve with noise to txt.file
    towrite = [indent; forcewithnoise];
    fname_i = strcat(fname, '_+noise_', string(i), '.txt');
    fileID = fopen(fname_i, 'w');
    fprintf(fileID, '%6s %6s %6s %12.8f %12.8f %12.8f\n', 'E1', 'E2', 'h', E1, E2, h);
    fprintf(fileID, '%6s %12s\n', 'x', 'F');
    fprintf(fileID, '%6.2f %12.8f\n', A);
    fclose(fileID);
% 
%     % plot the FD curve
%     plot(fc.ext(1:end,1), fc.ext(:,2), 'linewidth',2);
%     ylabel('Force [N]');
%     xlabel('Indentation Depth [m]');
%     set(gca,'fontsize',16);
%     % fit each point to Hertz model
%     plot(fc.ext(2:end,1), (3/4).*(1-nu1^2).*fc.ext(2:end,1).^(-3/2).*r.^(-1/2).*fc.ext(2:end,2),'linewidth',2);
%     ylabel('Apparent E [Pa]');
%     xlabel('Indentation Depth [m]');
%     set(gca,'fontsize',16);

end