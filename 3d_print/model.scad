pizero_height = 10;
pizero_width = 65;
pizero_length = 30;
pizero_hole_r = 2.25/2;
pi_header_width = 51;
pi_header_length = 5;

a = 80;
b = 35;
border_radius = 2.5;
wall_thickness = 1.6;

part="top"; /* base or top */
pir=true;
lux=false;

module corner(height=15, holes=true, hole_only=false) {
    module inner(r=1.25) {
        translate([0,0,wall_thickness]) {
            cylinder(h=(height), r=r, $fn=16);
        }
    }
    if(hole_only) {
        if (holes) {
            inner(r=1.75);
        }
    } else {
        cylinder(h=height, r=border_radius, $fn=16);
        inner();
    }
}

module corners(holes=true, holes_only=false) {
    for(i=[-1,1]) {
        for(j=[-1,1]) {
            translate([i*(a/2), j*(b/2)]) {
                corner(height=height, holes=holes, hole_only=holes_only);
            }
        }
    }
}

module pizero_connectors() {
    translate([0,-(b/2)-wall_thickness,pizero_height/2+wall_thickness]) {
        cube([pizero_width,wall_thickness*2, pizero_height], center=true);
    }
}

module pizero_holder() {
    translate([0, -(b/2)-wall_thickness+pizero_length/2, 0]) {
        translate([0,0,wall_thickness/2]) {
            cube([pizero_width, pizero_length, wall_thickness], center=true);
        }
        for (i=[-1,1]) {
            for (j=[-1,1]) {
                translate([i*pizero_width/2-i*3.5, j*pizero_length/2-j*3.5, wall_thickness])
                cylinder(h=2, r=pizero_hole_r, $fn=16);
            }
        }
    }
}

module pizero_header_clearance() {
    translate([0,-(b/2)-wall_thickness+pizero_length-pi_header_length/2-1,wall_thickness]) {
        cube([pi_header_width, pi_header_length, 2], center=true);
    }
}

module ventilation() {
    for(i=[0, 8, 16, 24, 32]) {
        translate([-i,0]) {
            cube([3, b-5, 10], center=true);
        }
    }
}

module case(height=15, holes=true) {
    difference() {
        union() {
            // Corners
            corners(height=height, holes=holes);

            // Walls
            for(i=[-1,1]) {
                translate([0,-i*(b/2 + border_radius - wall_thickness/2), height/2]) {
                    cube([a, (wall_thickness), height], center=true);
                }
                rotate([0,0,90]) {
                    translate([0,-i*(a/2 + border_radius - wall_thickness/2), height/2]) {
                        cube([b, (wall_thickness), height], center=true);
                    }
                }
            }

            // Floor
            translate([-(a+border_radius)/2, -(b+border_radius)/2]) {
                cube([a+border_radius,b+border_radius,wall_thickness]);
            }
        }
        corners(height=height, holes=holes, holes_only=true);
    }
}

if (part == "base") {
    difference() {
        union() {
            case(height=8, holes=false);
            pizero_holder();
        }
        pizero_connectors();
        pizero_header_clearance();
    }
} else {
    arr=[];
    led_r = 5.5;
    lux_r = 4;
    pir_r = 23.5;
    difference() {
        union() {
            case(height=12, holes=true);
            for (i=[[(led_r + 1)/2, 35-led_r/2, -b/2+2+led_r/2], [(led_r + 1)/2, 35-pir_r+led_r/2, -b/2+2+led_r/2]]) {
                translate([i[1], i[2]]) {
                    cylinder(h=5, r=i[0], $fn=24);
                }
            }
            //cylinder(h=wall_thickness*3, r=lux_r+2, $fn=24);
        }
        ventilation();
        for(i=[[led_r/2, 35-led_r/2, -b/2+2+led_r/2], [led_r/2, 35-pir_r+led_r/2, -b/2+2+led_r/2]]) {
            translate([i[1], i[2]]) {
                cylinder(h=5, r=i[0], $fn=24);
            }
        }
        if (lux) {
                cylinder(h=5, r=lux_r, $fn=24);
        }
        if (pir){
            translate([35-pir_r/2, b/2-2-pir_r/2]) {
                cylinder(h=20, r=pir_r/2, $fn=24);
            }
        }
    }
}
