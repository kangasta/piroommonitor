pizero_height = 5;
pizero_width = 65;
pizero_length = 30;
pizero_hole_r = 2.7/2;
pi_header_width = 51;
pi_header_length = 5;

a = 80;
border_radius = 2;
wall_thickness = 1.6;
connector_wall_thickness = 0.5;

part="top_no_pir"; /* base or top or top_no_pir */

module corner(height=15, holes=true, hole_only=false) {
    module inner() {
        translate([0,0,wall_thickness]) {
            cylinder(h=(height), r=1.25, $fn=16);
        }
    }
    if(hole_only) {
        if (holes) {
            inner();
        }
    } else {
        cylinder(h=height, r=border_radius, $fn=16);
        inner();
    }
}

module corners(holes=true, holes_only=false) {
    for(i=[-1,1]) {
        for(j=[-1,1]) {
            translate([i*(a/2), j*(a/2)]) {
                corner(height=height, holes=holes, hole_only=holes_only);
            }
        }
    }
}

module pizero_connectors() {
    translate([0,-(a/2)-wall_thickness/2+connector_wall_thickness,pizero_height/2+wall_thickness]) {
        difference() {
            cube([pizero_width,wall_thickness, pizero_height], center=true);
            translate([0,-wall_thickness/2,pizero_height-wall_thickness]) {
                rotate([45, 0, 0]) {
                    cube([pizero_width,wall_thickness*2, wall_thickness*2], center=true);
                }
            }
        }
        for(i=[[13,12.4],[8,41.4],[8,54]]) {
            translate([-pizero_width/2+i[1],0,-pizero_height/2+3/2]) {
            cube([i[0], 10, 3],center=true);
        }
        }
    }
}

module pizero_holder() {
    translate([0, -(a/2)-wall_thickness+connector_wall_thickness+pizero_length/2, 0]) {
        translate([0,0,wall_thickness/2]) {
            cube([pizero_width, pizero_length, wall_thickness], center=true);
        }
        for (i=[-1,1]) {
            for (j=[-1,1]) {
                translate([i*pizero_width/2-i*3.5, j*pizero_length/2-j*3.5, wall_thickness])
                cylinder(h=1.5, r=pizero_hole_r, $fn=16);
            }
        }
    }
}

module pizero_header_clearance() {
    translate([0,-(a/2)-wall_thickness+connector_wall_thickness+pizero_length-pi_header_length/2-1,wall_thickness]) {
        cube([pi_header_width, pi_header_length, 2], center=true);
    }
}

module case(height=15, holes=true) {
    difference() {
        union() {
            // Corners
            corners(height=height, holes=holes);

            // Walls
            for(i=[-1,1]) {
                for(j=[0,90]) {
                    rotate([0,0,j]) {
                        translate([0,-i*(a/2 + border_radius - wall_thickness/2), height/2]) {
                            cube([a, (wall_thickness), height], center=true);
                        }
                    }
                }
            }

            // Floor
            translate([-(a+border_radius)/2, -(a+border_radius)/2]) {
                cube([a+border_radius,a+border_radius,wall_thickness]);
            }
        }
        corners(height=height, holes=holes, holes_only=true);
    }
}

/*
pizero_holder();
pizero_connectors();
pizero_header_clearance();
*/

///*
if (part == "base") {
    difference() {
        union() {
            case(height=15, holes=false);
            pizero_holder();
        }
        pizero_connectors();
        pizero_header_clearance();
    }
} else {
    difference() {
        case(height=5, holes=true);
        arr=[];
        if (part == "top_no_pir") {
            for(i=[[5, 0, 35-5], [5/2, -35/2, 35-5], [5/2, 35/2, 35-5]]) {
                translate([i[1], i[2]]) {
                    cylinder(h=5, r=i[0], $fn=24);
                }
            }
        } else if (part == "top"){
            for(i=[[5, 0, 35-5], [5/2, 35-5/2, 0], /*[5/2, 35-23/2, 0],*/ [5/2, 35-23+5/2, 0], [23/2, 35-23/2, 35-23/2]]) {
                translate([i[1], i[2]]) {
                    cylinder(h=5, r=i[0], $fn=24);
                }
            }
        }
    }
}
//*/