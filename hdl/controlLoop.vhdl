-- Control loop for demonstration of co simulation in python and cocotb
library ieee ;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity controlLoop is
port(
        clock_i : in std_logic;
        controlInput_i : in  signed(17 downto 0);
        kp_i : in  signed(3 downto 0);
        ki_i : in  signed(4 downto 0);
        feedback_o : out signed(17 downto 0);
        A : in  unsigned(DATA_WIDTH-1 downto 0);
        B : in  unsigned(DATA_WIDTH-1 downto 0);
        X : out unsigned(DATA_WIDTH downto 0)
    );
end controlLoop;

architecture RTL of controlLoop is
    signal proportional : signed(21 downto 0) := (others => '0');
    signal proportionalResized : signed(17 downto 0) := (others => '0');
    signal integrator : signed(18 downto 0)  := (others => '0');
    signal integral : signed(23 downto 0) := (others => '0');
    signal feedback : signed(17 downto 0) := (others => '0');

begin

    process(controlInput_i, kp_i)
    begin
        proportional <= controlInput_i * kp_i;
    end process;

    proportionalResized <= proportional(21 downto 4);

    process(proportionalResized)
    begin
        integrator <= resize(integrator, integrator'length) + proportionalResized;
    end process;

    process(integrator, ki_i)
    begin
        integral <= integrator * ki_i;
    end process;

    process(clock_i,controlInput_i)
    begin
        if(rising_edge(clock_i)) then
          feedback_o <= integral(23 downto 6);
        end if;
    end process;

end RTL;
