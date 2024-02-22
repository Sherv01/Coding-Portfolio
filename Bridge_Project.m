% Rows are pieces, columns are [width, height, dist_from_bot] 
% note: use distance from bottom of the cross section to bottom 
% of the piece and NOT the centroid of the piece
pieces = [
    [100 1.27 0]; % This is the triple top I beam
    [1.27 100 1.27];
    [100 1.27 101.27];
    [100 1.27 102.54];
    [100 1.27 103.81]
];
% pieces = [
%     [1.27 100 0]; % This is the Example from class
%     [1.27 100 0];
%     [10 1.27 98.73];
%     [10 1.27 98.73];
%     [120 1.27 100];
%     [120 1.27 101.27]
% ];
% pieces = [
%     [120 1.27 0]; % This is the square HSS with the double top (120x120)
%     [1.27 117.46 1.27];
%     [7.5 1.27 117.46];
%     [118.73 1.27 118.73];
%     [1.27 118.73 1.27];
%     [120 1.27 120]
% ];
% pieces = [
%     [100 1.27 0]; % This is the rectangle HSS with the double top (100x120)
%     [1.27 117.46 1.27];
%     [1.27 118.73 1.27];
%     [15 1.27 117.46];
%     [98.73 1.27 118.73];
%     [100 1.27 120] % FINAL DESIGN
% ];
% pieces = [
%     [120 1.27 0]; % This is the rectangle HSS (120x140)
%     [1.27 137.46 1.27];
%     [1.27 138.73 1.27];
%     [7.5 1.27 137.46];
%     [188.73 1.27 138.73]
% ];
% pieces = [
%     [100 1.27 0]; % This is the square HSS with a horizontal member in it
%     [1.27 97.46 1.27];
%     [1.27 97.46 1.27];
%     [50 1.27 98.73];
%     [50 1.27 98.73];
%     [100 1.27 100];
%     [97.46 1.27 1.27];
%     [1.27 5 50];
%     [1.27 5 50] 
% ];

% Design 0
pieces = [
    [80 1.27 0];
    [1.27 73.73 1.27];
    [1.27 73.73 1.27];
    [5 1.27 73.73];
    [5 1.27 73.73];
    [100 1.27 75]
];
total_area = 0;
weighted_centroid_sum = 0;

% First loop to calculate ybar
for i = 1:size(pieces, 1)
    width = pieces(i, 1);
    height = pieces(i, 2);
    distance_from_bottom = pieces(i, 3);

    % Calculate area and centroid of this piece
    area = width * height;
    centroid = distance_from_bottom + (height / 2);

    % Update total area and weighted centroid sum
    total_area = total_area + area;
    weighted_centroid_sum = weighted_centroid_sum + area * centroid;
end
ybar = weighted_centroid_sum / total_area;
I = 0;

% Second loop to calculate I
for i = 1:size(pieces, 1)
    width = pieces(i, 1);
    height = pieces(i, 2);
    distance_from_bottom = pieces(i, 3);

    % Calculate area and centroid of this piece
    area = width * height;
    centroid = distance_from_bottom + height / 2;

    % Calculate and add the moment of inertia of this piece
    I_piece = ((width * height^3) / 12) + area * (centroid - ybar)^2;
    I = I + I_piece;
end

% Calculate ybot and ytop
ybot = ybar - min(pieces(:, 3));
ytop = max(pieces(:, 3) + pieces(:, 2)) - ybar;
Qcent = calculate_Q(pieces, ybar);
Qglue = [];

for i = 1 : size(pieces, 1)
    if i == size(pieces, 1)
        continue;
    end
    Qglue(i) = calculate_Q(pieces, pieces(i + 1, 3));
end

total_area
ybar
I
Qcent
Qglue % The matrix can be interpreted as the
% glue shear stress between one piece and the piece 
% that follows it the pieces matrix.
% if two pieces are not glued together, ignore the produced Q value

load_case = input("Which load case would you like? (Enter 1 or 2)");

if load_case == 1
    V = 256.6795;
    M = 69442;
elseif load_case == 2
    V = 299.84;
    M = 77162.7;
end

SigmaComp = (M .* -ytop) ./ I
SigmaTens = (M .* ybar) ./ I
TauCent = (V .* Qcent) ./ (I .* 2.54)
TauGlue = (V .* Qglue) ./ (I .* 10)
t = 1.27;
h = 72.46;
a = 400;

SigmaBuck4 = ((4 .* (pi .^2) .* 4000) ./ (12 .* (1 - (0.2) .^ 2))) .* (t ./ 70) .^2;
SigmaBuck0425 = ((0.425 .* (pi .^ 2) .* 4000) ./ (12 .* (1 - (0.2) .^ 2))) .* (1.27 ./ 15) .^2;
SigmaBuck6 = ((6 .* (pi .^ 2) .* 4000) ./ (12 .* (1 - (0.2) .^ 2))) .* (1.27 ./ ytop) .^2;
SigmaBuck5 = ((5 .* (pi .^ 2) .* 4000) ./ (12 .* (1 - (0.2) .^ 2))) .* ((1.27 ./ h) .^2 + ((1.27 ./ a) .^2));

% The numbers on the SigmaBuck represent the value of k
FOS_comp = 6 ./ -SigmaComp
FOS_tens = 30 ./ SigmaTens
FOS_shearcent = 4 ./ TauCent
FOS_shearglue = 2 ./ TauGlue
FOS_buck4 = SigmaBuck4 ./ -SigmaComp
FOS_buck0425 = SigmaBuck0425 ./ -SigmaComp
FOS_buck6 = SigmaBuck6 ./ -SigmaComp
FOS_buck5 = SigmaBuck5 ./ TauCent

% Calculate Qcent and Qglue
function Q = calculate_Q(pieces, depth)
    total_area = 0;
    weighted_centroid_sum = 0;

    % First loop to calculate ybar
    for i = 1:size(pieces, 1)
        width = pieces(i, 1);
        height = pieces(i, 2);
        distance_from_bottom = pieces(i, 3);

        % Calculate area and centroid of this piece
        area = width * height;
        centroid = distance_from_bottom + height / 2;

        % Update total area and weighted centroid sum
        total_area = total_area + area;
        weighted_centroid_sum = weighted_centroid_sum + area * centroid;
    end

    % Calculate ybar
    ybar = weighted_centroid_sum / total_area;
    A = 0;
    Q = 0;

    % Second loop to calculate A and Q
    for i = 1:size(pieces, 1)
        width = pieces(i, 1);
        height = pieces(i, 2);
        distance_from_bottom = pieces(i, 3);

        % If the depth of interest (DOI) is above the centroidal axis
        if depth > ybar
            % If the piece is entirely above the DOI, include it entirely
            if distance_from_bottom >= depth
                A = width * height;
                centroid = distance_from_bottom + height / 2;
            % If the DOI is in the piece, include only the part above the DOI
            elseif distance_from_bottom < depth && distance_from_bottom + height > depth
                A = width * (distance_from_bottom + height - depth);
                centroid = depth + (distance_from_bottom + height - depth) / 2;
            else
                centroid = ybar;
            end
        % If the DOI is below the centroidal axis
        else
            % If the piece is entirely below the DOI, include it entirely
            if distance_from_bottom + height <= depth
                A = width * height;
                centroid = distance_from_bottom + height / 2;
            % If the DOI is in the piece, include only the part below the DOI
            elseif distance_from_bottom < depth && distance_from_bottom + height > depth
                A = width * (depth - distance_from_bottom);
                centroid = distance_from_bottom + ((depth - distance_from_bottom) / 2);
            else
                centroid = ybar;
            end
        end
        % Calculate Q
        Q = Q + (A * abs(ybar - centroid));
    end
end
